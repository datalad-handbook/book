#!/bin/bash
# =============================================================================
# Kedro vs DataLad Handbook Examples Test Script
# =============================================================================
#
# This script tests all commands from the Kedro comparison section of the
# DataLad Handbook (101-185-kedro.rst).
#
# Requirements:
#   - Python 3.8+
#   - pip (or uv)
#   - git
#   - datalad (pip install datalad)
#   - Internet connection (for cloning subdatasets)
#
# Installation (if needed):
#   pip install datalad kedro pandas
#
# Usage:
#   ./kedro-examples-test.sh [--cleanup] [--skip-kedro]
#
# Options:
#   --cleanup      Remove test directory after successful run
#   --skip-kedro   Skip Kedro-specific tests (test DataLad parts only)
#
# Environment:
#   DATALAD_CMD    Path to datalad executable (default: datalad)
#   PYTHON_CMD     Path to python executable (default: python3 or python)
#
# =============================================================================

set -e  # Exit on error

# Configuration
TEST_DIR="${TMPDIR:-/tmp}/kedro-datalad-test-$$"
CLEANUP=false
SKIP_KEDRO=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --cleanup)
            CLEANUP=true
            shift
            ;;
        --skip-kedro)
            SKIP_KEDRO=true
            shift
            ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo "============================================================================="
    echo "$1"
    echo "============================================================================="
}

# Cleanup function
cleanup() {
    if [ "$CLEANUP" = true ] && [ -d "$TEST_DIR" ]; then
        log_info "Cleaning up test directory: $TEST_DIR"
        rm -rf "$TEST_DIR"
    else
        log_info "Test directory preserved at: $TEST_DIR"
    fi
}

trap cleanup EXIT

# =============================================================================
# SETUP
# =============================================================================
log_section "Setting up test environment"

log_info "Creating test directory: $TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Check prerequisites
log_info "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    log_error "git is not installed"
    exit 1
fi

# Allow specifying datalad path via environment
DATALAD="${DATALAD_CMD:-datalad}"
if ! command -v "$DATALAD" &> /dev/null; then
    # Try to find datalad in common locations
    for loc in ~/.local/bin/datalad ~/miniconda3/bin/datalad /usr/local/bin/datalad; do
        if [ -x "$loc" ]; then
            DATALAD="$loc"
            break
        fi
    done
    if ! command -v "$DATALAD" &> /dev/null && [ ! -x "$DATALAD" ]; then
        log_error "datalad is not installed or not found in PATH"
        log_error "Install with: pip install datalad"
        log_error "Or set DATALAD_CMD environment variable to the path"
        exit 1
    fi
fi
log_info "Using datalad: $DATALAD"

# Allow specifying python path via environment
PYTHON="${PYTHON_CMD:-}"
if [ -z "$PYTHON" ]; then
    if command -v python3 &> /dev/null; then
        PYTHON=python3
    elif command -v python &> /dev/null; then
        PYTHON=python
    else
        log_error "python is not installed"
        exit 1
    fi
fi
log_info "Using Python: $PYTHON"

# Create alias function for datalad
datalad() {
    "$DATALAD" "$@"
}

# Create a virtual environment for Kedro
log_info "Creating virtual environment..."
$PYTHON -m venv venv
source venv/bin/activate

log_info "Installing required packages..."
pip install --quiet --upgrade pip
pip install --quiet kedro pandas

# Verify kedro is installed
if ! command -v kedro &> /dev/null; then
    log_error "kedro installation failed"
    exit 1
fi
log_info "Kedro version: $(kedro --version)"

# =============================================================================
# TEST 1: DataLad Setup (YODA structure)
# =============================================================================
log_section "TEST 1: DataLad YODA Setup"

log_info "Creating DataLad dataset with YODA configuration..."

### DataLad
datalad create -c yoda -c text2git my-analysis
cd my-analysis
mkdir -p data/{raw,intermediate,processed} model metrics

log_info "Verifying directory structure..."
if [ -d "code" ] && [ -d "data/raw" ] && [ -d "data/intermediate" ] && [ -d "data/processed" ]; then
    log_info "PASS: DataLad YODA structure created correctly"
else
    log_error "FAIL: Directory structure is incorrect"
    exit 1
fi

cd "$TEST_DIR"

# =============================================================================
# TEST 2: DataLad Subdatasets
# =============================================================================
log_section "TEST 2: DataLad Subdatasets"

log_info "Creating a superdataset..."
datalad create -c yoda superdataset-demo
cd superdataset-demo

log_info "Adding iris_data as a subdataset..."
### DataLad: Add data as a subdataset
datalad clone -d . \
    https://github.com/datalad-handbook/iris_data \
    data/raw/iris

log_info "Checking subdatasets..."
### DataLad: Check subdataset versions
datalad subdatasets

# Verify subdataset was added
if [ -d "data/raw/iris/.datalad" ]; then
    log_info "PASS: Subdataset added correctly"
else
    log_error "FAIL: Subdataset not added correctly"
    exit 1
fi

cd "$TEST_DIR"

# =============================================================================
# TEST 3: Kedro + DataLad Combined Workflow
# =============================================================================
if [ "$SKIP_KEDRO" = true ]; then
    log_section "TEST 3: SKIPPED (Kedro + DataLad Combined Workflow)"
    log_warn "Skipping Kedro tests as requested"
else
log_section "TEST 3: Kedro + DataLad Combined Workflow"

log_info "Creating DataLad dataset for Kedro project..."

### Create a DataLad dataset with YODA configuration
datalad create -c yoda -c text2git kedro-datalad-demo
cd kedro-datalad-demo

log_info "Creating minimal Kedro project structure..."

### Create minimal Kedro structure
mkdir -p src/demo_pipeline
touch src/demo_pipeline/__init__.py

log_info "Creating pyproject.toml with Kedro configuration..."

# Note: We append to the existing pyproject.toml or create one
cat >> pyproject.toml << 'EOF'

[tool.kedro]
package_name = "demo_pipeline"
project_name = "demo_pipeline"
kedro_init_version = "1.2.0"
source_dir = "src"
EOF

log_info "Creating settings.py..."
cat > src/demo_pipeline/settings.py << 'EOF'
# Kedro settings
EOF

log_info "Creating pipeline_registry.py with demo pipeline..."
cat > src/demo_pipeline/pipeline_registry.py << 'EOF'
from kedro.pipeline import Pipeline, node

def greet(name: str) -> str:
    greeting = f"Hello, {name}!"
    # Write output for provenance tracking
    with open("output.txt", "w") as f:
        f.write(greeting)
    return greeting

def register_pipelines():
    return {
        "__default__": Pipeline([
            node(greet, inputs="params:name", outputs="greeting")
        ])
    }
EOF

log_info "Creating configuration directories and parameters..."
mkdir -p conf/base conf/local
cat > conf/base/parameters.yml << 'EOF'
name: DataLad
EOF

cat > conf/base/catalog.yml << 'EOF'
# Empty catalog (required by Kedro 1.x)
EOF

log_info "Creating .gitignore for Python cache files..."
cat >> .gitignore << 'EOF'
__pycache__/
*.pyc
EOF

log_info "Saving Kedro project structure to DataLad..."
### Track Kedro project structure
datalad save -m "Initialize minimal Kedro project"

log_info "Running Kedro pipeline with DataLad provenance..."
# Disable telemetry for cleaner output
export KEDRO_DISABLE_TELEMETRY=true
### Run Kedro pipeline with DataLad provenance
datalad run \
    --message "Execute Kedro demo pipeline" \
    --output "output.txt" \
    kedro run

# Check that the output file was created
if [ -f "output.txt" ]; then
    log_info "PASS: Pipeline generated output.txt"
    content=$(cat output.txt)
    if [ "$content" = "Hello, DataLad!" ]; then
        log_info "PASS: Output content is correct"
    else
        log_warn "Output content: $content"
    fi
else
    log_error "FAIL: No output.txt file generated"
    exit 1
fi

# Check that the run was recorded
if git log --oneline -1 | grep -q "Execute Kedro demo pipeline"; then
    log_info "PASS: Kedro pipeline run recorded in Git history"
else
    log_error "FAIL: Pipeline run not recorded correctly"
    exit 1
fi

log_info "Adding data subdataset..."
### Add shared data as subdataset
datalad clone -d . \
    https://github.com/datalad-handbook/iris_data \
    data/01_raw/iris

# Verify subdataset
if [ -d "data/01_raw/iris/.datalad" ]; then
    log_info "PASS: Data subdataset added"
else
    log_error "FAIL: Data subdataset not added"
    exit 1
fi

log_info "Creating catalog.yml with iris data reference..."
cat > conf/base/catalog.yml << 'EOF'
iris_data:
  type: pandas.CSVDataset
  filepath: data/01_raw/iris/iris.csv
EOF

datalad save -m "Add iris data subdataset and catalog configuration"

cd "$TEST_DIR"
fi  # End of SKIP_KEDRO check for TEST 3

# =============================================================================
# TEST 4: Kedro Standalone (for reference)
# =============================================================================
if [ "$SKIP_KEDRO" = true ]; then
    log_section "TEST 4: SKIPPED (Kedro Standalone Project)"
    log_warn "Skipping Kedro tests as requested"
else
log_section "TEST 4: Kedro Standalone Project (Reference)"

log_info "Creating a standalone Kedro minimal project..."
mkdir -p kedro-standalone
cd kedro-standalone

# Create minimal Kedro project structure
mkdir -p src/standalone_demo
touch src/standalone_demo/__init__.py

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "standalone_demo"
version = "0.1.0"

[tool.kedro]
package_name = "standalone_demo"
project_name = "standalone_demo"
kedro_init_version = "1.2.0"
source_dir = "src"
EOF

cat > src/standalone_demo/settings.py << 'EOF'
# Kedro settings
EOF

cat > src/standalone_demo/pipeline_registry.py << 'EOF'
from kedro.pipeline import Pipeline, node

def add_numbers(a: int, b: int) -> int:
    return a + b

def register_pipelines():
    return {
        "__default__": Pipeline([
            node(add_numbers, inputs=["params:a", "params:b"], outputs="sum_result")
        ])
    }
EOF

mkdir -p conf/base conf/local
cat > conf/base/parameters.yml << 'EOF'
a: 5
b: 3
EOF

cat > conf/base/catalog.yml << 'EOF'
# Empty catalog (required by Kedro 1.x)
EOF

log_info "Running standalone Kedro project..."
export KEDRO_DISABLE_TELEMETRY=true
kedro run

if [ $? -eq 0 ]; then
    log_info "PASS: Standalone Kedro project runs successfully"
else
    log_error "FAIL: Standalone Kedro project failed"
    exit 1
fi

cd "$TEST_DIR"
fi  # End of SKIP_KEDRO check for TEST 4

# =============================================================================
# SUMMARY
# =============================================================================
log_section "TEST SUMMARY"

echo ""
log_info "All tests passed successfully!"
echo ""
echo "Test artifacts created in: $TEST_DIR"
echo ""
echo "Contents:"
ls -la "$TEST_DIR"
echo ""

if [ "$CLEANUP" = true ]; then
    log_info "Cleanup requested - test directory will be removed"
else
    echo "To clean up manually, run:"
    echo "  rm -rf $TEST_DIR"
fi

echo ""
log_info "Test script completed successfully!"

Redirection
-----------

This page exists for redirection purposes only.

..
   Include a named paragraph in the page, where the javascript code below will
   place any message.

.. raw:: html

   <p><strong id="successmessage">
     You will be redirected to your target page in a few seconds.
   </strong></p>

.. figure:: artwork/src/redirection.svg

..
   use a custom role to identify redirect codes so that a bit of JS can find
   them again

.. role:: redirect
   :class: redirect

If you continue to see this page, you've ended up in here accidentally and redirection
failed -- sorry about this.

**Here are some links that may take you to where you need to go:**

..
   This defines a mapping of redirect codes to their present URLs.
   Please keep sorted by redirection label.

:redirect:`ABCD`
  :ref:`abcd`
:redirect:`about`
  :ref:`executive_summary`
:redirect:`cheatsheet`
  :ref:`cheat`
:redirect:`clone-priority`
  :ref:`cloneprio`
:redirect:`containers`
  :ref:`containersrun`
:redirect:`dataladdening`
  :ref:`dataladdening`
:redirect:`dl-for-ml`
  :ref:`dvc`
:redirect:`dgpa`
  :ref:`dgpa`
:redirect:`extensions`
  :ref:`extensions_intro`
:redirect:`filenaming`
  :ref:`filenaming`
:redirect:`GIN`
  :ref:`gin`
:redirect:`gobig`
  :ref:`chapter_gobig`
:redirect:`LFS`
  :ref:`gitlfs`
:redirect:`HCP-dataset`
  :ref:`usecase_HCP_dataset`
:redirect:`install`
  :ref:`install`
:redirect:`reproducible-paper`
  :ref:`usecase_reproducible_paper`
:redirect:`RIA`
  :ref:`riastore`
:redirect:`runhpc`
  :ref:`runhpc`
:redirect:`yoda`
  :ref:`yoda`
:redirect:`OHBM2020`
  :ref:`OHBMOSR2020`
:redirect:`OHBM2020poster`
  :ref:`ohbm2020poster`
:redirect:`ml-usecase`
  :ref:`usecase_ML`
:redirect:`openneuro`
  :ref:`openneuro`
:redirect:`FZJmlcode`
  :ref:`mlcode`
:redirect:`MPIBerlin`
  :ref:`mpiberlin`
:redirect:`Yale`
  :ref:`yale`

Alternatively, try searching in the "Quick Search" at the left-hand side, or
scan the handbook's front page at `handbook.datalad.org <http://handbook.datalad.org/en/latest/>`_
for directions.

..
   This code replaces the r.html?key part with the final URL, while keeping
   the rest of URL intact.

.. raw:: html

   <script>
   // take everything after "?" as a code to identify the redirect. If there is a '=' appended (a glitch that started to surface Dec 2022), remove it and everything afterwards
   redirect_code = window.location.href.replace(/.*\?/, "").replace(/=.*/, "");
   success = false;
   // loop over all redirect definitions (see above)
   for (rd of document.getElementsByClassName('redirect')){
     if (rd.innerText != redirect_code) {continue;}
     // read the href from the link in the <dd> matching the <dt> of the redirect
     // this assumes a very simple, and particular structure
     // let's hope that sphinx doesn't break it
     target = rd.parentElement.nextElementSibling.getElementsByTagName("a")[0].href;
     // and jump
     window.location.replace(target);
     success = true;
     break;
   }
   // if we get here, we didn't find a match
   if (success == false) {
     document.getElementById("successmessage"
       ).innerHTML = "Whoops - redirection went wrong, we are lost!"
   }
   </script>

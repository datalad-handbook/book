Redirection
-----------


.. raw:: HTML

   <html>
     <head>
        <p id="demo"></p>

        <script>
        let redirects = new Map([
            ['demo', 'url1'],
            ['#GIN', 'basics/101-139-gin.html']
        ]);
        redirect = redirects.get(window.location.hash);
        if (redirect == undefined) {
          document.getElementById("demo").innerHTML = "no idea"
        } else {
          window.location.href.replace(/r.html.*/, redirect)
        }
        </script>
     </head>
   </html>

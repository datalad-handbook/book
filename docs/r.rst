Redirection
-----------

..
   Include a named paragraph in the page, where the javascript code below will
   place any message.

.. raw:: html

   <p id="message"></p>

..
   This defines a mapping of redirect codes to their present URLs

.. raw:: html

   <script>
   let redirects = new Map([
       ['GIN', 'basics/101-139-gin.html'],
       ['HCP-dataset', 'usecases/HCP_dataset.html'],
       ['reproducible-paper', 'usecases/reproducible-paper.html']
   ]);
   </script>

..
   This code replaces the r.html?key part with the final URL, while keeping
   the rest of URL intact.

.. raw:: html

   <script>
   redirect = redirects.get(window.location.href.replace(/.*\?/, ""));
   if (redirect == undefined) {
     document.getElementById("demo").innerHTML = "no idea"
   } else {
     window.location.replace(window.location.href.replace(/r.html\?.*/, redirect))
   }
   </script>

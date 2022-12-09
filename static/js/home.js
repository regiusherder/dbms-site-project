$(document).ready(function () {

    var settings = {
      "async": true,
      "crossDomain": true,
      "url": "common",
      "method": "GET",
      "headers": {
        "cache-control": "no-cache"
      }
    }
  
    $.ajax(settings).done(function (response) {
      console.log(response);
      $('#projectcount').text(response.project)
    });
  
  
  })
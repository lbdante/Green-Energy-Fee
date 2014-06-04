console.log('Loading a web page');
 
var page = require('webpage').create();
var name = "OM";
var url = "http://140.160.141.163/website/?building=" + name;
page.viewportSize = { width: 2000, height: 768 };
page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to access the network!'); 
		phantom.exit();
    } else {
          window.setTimeout(function () {
            page.render(name + '.png');
			phantom.exit();
        }, 1000);
    }
   
});

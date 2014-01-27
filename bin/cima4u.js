var page = require('webpage').create(),
	system = require('system'),
	address;

page.onConsoleMessage = function(msg){
		console.log(msg);
};

if (system.args.length === 1) {
	console.log('Usage: cima4u.js <some URL>');
	phantom.exit(1);
}
else{
	address = system.args[1];
	page.open(address,function (status) {
		if (status !== 'success') {
			console.log('FAIL to load the address');
		} else {
			var ret = page.evaluate(function(){
				$("table.art_content").each(function(i,val){
				    //抓取影片title、下载量和海报url
					console.log('Title:'+$(val).find("a.title_a").text());
					console.log('Num:'+$(val).find("a.dwn_a").text().match(/\d+/));
					console.log('Img:'+$(val).find("img.art_image_1").attr("src"));
					console.log("------------");
					})
					return 'end';
			});
			console.log(ret);
		}
		phantom.exit();
	});
}
/*
t = Date.now();
address = phantom.args[0];
page.open(address, function (status) {
	if (status !== 'success') {
		console.log('FAIL to load the address');
	} else {
		t = Date.now() - t;
		console.log('Loading time ' + t + 'msec');
	}
	phantom.exit();
});
*/

var system = require('system');
var args = system.args;	// username/pass
var page = new WebPage();
var testindex = 0;	// the current step of operations
var loadInProgress = false;

var username = args[1];
var pass = args[2];

var steps = [
	function() {
		// Load page that logs in to grades page
		page.open("https://campus.concordia.ca/psp/pscsprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL");
	},
	function() {
		// Enter credentials, log in
		page.evaluate(function(u, p) {	// receives username and pass as args
			document.getElementById("userid").value = u;
			document.getElementById("pwd").value = p;
			document.getElementsByClassName("form_button_submit")[0].click();
			return;
		}, username, pass);
	},
	function() {
		// Get link for and go to semester-selection form for grades
		var iFrameSrc = page.evaluate(function() {
			var isrc = document.getElementById("ptifrmtgtframe").src;
			return isrc;
		});
		page.open(iFrameSrc);
	},
	function() {
		// Select semester and submit form
		page.evaluate(function() {
			document.getElementById("SSR_DUMMY_RECV1$sels$2$$0").checked = true;
			submitAction_win0(document.win0,'DERIVED_SSS_SCT_SSR_PB_GO');
			return;
		});
	},
	function() {
		page.evaluate(function() {
			// for all grades in table
			for(j = 0; !!document.getElementById("win0divDERIVED_SSS_HST_DESCRSHORT$" + j); j++) {
				// Output: "[Course-code]: [grade]"
				var grade = document.getElementById("win0divDERIVED_SSS_HST_DESCRSHORT$" + j).childNodes[0].innerHTML;
				grade = grade.replace(/( |\&nbsp;|\,)/g,'');	// remove odd characters from the grade string
				console.log(document.getElementById("CLS_LINK$" + j).innerHTML + ": " + grade);
			}
		});
	}
];

interval = setInterval(function() {
	if (!loadInProgress && typeof steps[testindex] == "function") {
		steps[testindex]();
		testindex++;
	}
	if (typeof steps[testindex] != "function") {
		phantom.exit();
	}
}, 1000);

page.onConsoleMessage = function(msg) {
	console.log(msg);
};

// Suppress error output
page.onError = function() {
	// do nothing
}

page.onLoadStarted = function() {
	loadInProgress = true;
};

page.onLoadFinished = function() {
	loadInProgress = false;
};

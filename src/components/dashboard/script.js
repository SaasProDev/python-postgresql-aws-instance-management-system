angular.module('myApp').controller('CardDemoCtrl', function ($scope, $window, $timeout) {
  var imagePath = $window.IMAGE_PATH || "img";

  $scope.dataLoading = true;

  $scope.status = {
    "title": "Nodes",
    "href": "#",
    "iconClass": "fa fa-shield",
    "notifications": []
  };

  $scope.status2 = {
    "title": "Nodes",
    "count": 793,
    "href": "#",
    "iconClass": "fa fa-shield",
    "notifications": [
      {
        "iconClass": "pficon pficon-error-circle-o",
        "count": 4,
        "href": "#"
      },
      {
        "iconClass": "pficon pficon-warning-triangle-o",
        "count": 1
      }
    ]
  };
  $scope.aggStatusAlt = {
    "title": "Providers",
    "count": 3,
    "notifications": [
      {
        // "iconImage": imagePath + "/kubernetes.svg",
        "iconClass": "pficon pficon-warning-triangle-o",
        "count": 1,
        "href": "#"
      },
      {
        // "iconImage": imagePath + "/OpenShift-logo.svg",
        "iconClass": "pficon pficon-warning-triangle-o",
        "count": 2,
        "href": "#"
      }
    ]
  };

  $scope.aggStatusAlt2 = {
    "title": "Providers",
    "notifications": []
  };

  $timeout(function () {
    $scope.dataLoading = false;

    $scope.status = {
      "title": "Nodes",
      "count": 793,
      "href": "#",
      "iconClass": "fa fa-shield",
      "notifications": [
        {
          "iconClass": "pficon pficon-error-circle-o",
          "count": 4,
          "href": "#"
        },
        {
          "iconClass": "pficon pficon-warning-triangle-o",
          "count": 1
        }
      ]
    };

    $scope.aggStatusAlt2 = {
      "title": "Providers",
      "count": 3,
      "notifications": [
        {
          // "iconImage": imagePath + "/kubernetes.svg",
          "iconClass": "pficon pficon-warning-triangle-o",
          "count": 1,
          "href": "#"
        },
        {
          // "iconImage": imagePath + "/OpenShift-logo.svg",
          "iconClass": "pficon pficon-warning-triangle-o",
          "count": 2,
          "href": "#"
        }
      ]
    };
  }, 6000);

  $scope.miniAggStatus = {
    "iconClass": "pficon pficon-container-node",
    "title": "Nodes",
    "count": 52,
    "href": "#",
    "notification": {
      "iconClass": "pficon pficon-error-circle-o",
      "count": 3
    }
  };

  $scope.miniAggStatus2 = {
    "iconClass": "pficon pficon-cluster",
    "title": "Adipiscing",
    "count": 9,
    "href": "#",
    "notification": {
      "iconClass": "pficon pficon-ok"
    }
  };

  //
  var term = new Terminal();
    term.open(document.getElementById('terminal'));
    term.write('CardDemoCtrl - Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ');


  var Client = require('ssh2').Client;
   
  var conn = new Client();
  conn.on('ready', function() {
    console.log('Client :: ready');
    conn.exec('uptime', function(err, stream) {
      if (err) throw err;
      stream.on('close', function(code, signal) {
        console.log('Stream :: close :: code: ' + code + ', signal: ' + signal);
        conn.end();
      }).on('data', function(data) {
        console.log('STDOUT: ' + data);
      }).stderr.on('data', function(data) {
        console.log('STDERR: ' + data);
      });
    });
  }).connect({
    host: '192.168.100.100',
    port: 22,
    username: 'frylock',
    privateKey: require('fs').readFileSync('/here/is/my/key')
  });
  

  //
});





angular.module('patternfly.charts').controller('ChartCtrl', function ($scope) {
  $scope.used = 950;
  $scope.total = 1000;
  $scope.available = $scope.total - $scope.used;

  $scope.chartConfig = patternfly.c3ChartDefaults().getDefaultDonutConfig('MHz Used');
  $scope.chartConfig.data = {
    type: "donut",
    columns: [
      ["Used", $scope.used],
      ["Available", $scope.total - $scope.used]
    ],
    groups: [
      ["used", "available"]
    ],
    order: null
  };

  $scope.getChart = function (chart) {
    $scope.chart = chart;
  };

  $scope.focusUsed = function () {
    $scope.chart.focus("Used");
  };

  $scope.updateAvailable = function (val) {
    $scope.available = $scope.total - $scope.used;
  };

  $scope.submitform = function (val) {
    console.log("submitform");
    $scope.used = val;
    $scope.updateAvailable();
    $scope.chartConfig.data.columns = [["Used", $scope.used], ["Available", $scope.available]];
  };
});





angular.module('patternfly.charts').controller('CardDemoTerminalCtrl', function ($scope) {

    var term = new Terminal();
    term.open(document.getElementById('terminal'));
    // // Terminal.applyAddon(fit);
    // // term.fit();

    // // var io = require('socket.io')(server);
    // // var SSHClient = require('ssh2').Client;
    // var conn = new Client();
    // conn.on('ready', function() {
    //   console.log('Client :: ready');
    //   conn.exec('uptime', function(err, stream) {
    //     if (err) throw err;
    //     stream.on('close', function(code, signal) {
    //       console.log('Stream :: close :: code: ' + code + ', signal: ' + signal);
    //       conn.end();
    //     }).on('data', function(data) {
    //       console.log('STDOUT: ' + data);
    //     }).stderr.on('data', function(data) {
    //       console.log('STDERR: ' + data);
    //     });
    //   });
    // }).connect({
    //   host: '192.168.100.100',
    //   port: 22,
    //   username: 'frylock',
    //   // privateKey: require('fs').readFileSync('/here/is/my/key')
    // });


    // var socket = io.connect("http://localhost:1001");
    //     socket.on("connect", function () {
    //         term.attach(socket);
    //     });

    // socket.on('connect', function() {
    //   term.write('\r\n*** Connected to backend***\r\n');

    //   // Browser -> Backend
    //   term.on('data', function(data) {
    //     socket.emit('data', data);
    //   });

    //   // Backend -> Browser
    //   socket.on('data', function(data) {
    //     term.write(data);
    //   });

    //   socket.on('disconnect', function() {
    //     term.write('\r\n*** Disconnected from backend***\r\n');
    //   });
    // });

    term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')



});

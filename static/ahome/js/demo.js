angular.module('patternfly.navigation').controller('showDemoController', ['$scope',
function ($scope) {
    $scope.showVerticalNav = function () {
      angular.element(document.querySelector("#verticalNavWithRouterLayout")).removeClass("hidden");
    };
  }
]);


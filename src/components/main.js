angular.module('myApp', ['patternfly.navigation', 'patternfly.charts', 'patternfly.table', 'patternfly.canvas', 'patternfly.card', 'ui.router'])
  .config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('dashboard');

    $stateProvider
      .state('dashboard', {
        url: '/dashboard',
        templateUrl: '/frontend/dashboard/'
      })
      .state('iaas', {
        url: '/iaas',
        templateUrl: '/frontend/iaas/'
      })
      .state('iaas-wizard-create', {
        url: '/iaas-wizard-create',
        templateUrl: 'frontend/iaas/wizardbox/create/'
      })
      .state('paas', {
        url: '/paas',
        templateUrl: '/frontend/paas/'
      })
      .state('paas-create', {
        url: '/paas-wizard-create',
        templateUrl: 'frontend/paas/create/'
      })
      .state('paas-detail', {
        url: '/paas-detail',
        templateUrl: 'frontend/paas/detail/'
      })
      .state('paas-platforms', {
        url: '/paas-platforms',
        templateUrl: 'frontend/paas/platforms/'
      })
      .state('credentials', {
        url: '/credentials',
        templateUrl: '/frontend/usercredentials/'
      })
      .state('secrets', {
        url: '/secrets',
        templateUrl: '/frontend/usersecrets/'
      })
      .state('admin-dashboard', {
        url: '/admin/dashboard',
        templateUrl: '/frontend/dashboard/user/'
      })
      .state('admin-organizations', {
        url: '/admin/organizations',
        templateUrl: '/frontend/organizations/'
      })
      .state('admin-users', {
        url: '/admin/users',
        templateUrl: '/frontend/users/'
      })

      .state('help', {
        url: '/help',
        template: '<div class="card-pf card-pf-accented card-pf-aggregate-status" style="height: 89px;">\
                          <div class="card-pf-body" style="height: 50px;">\
                            <p class="card-pf-aggregate-status-notifications">\
                              State: Help\
                            </p>\
                          </div>\
                        </div>'
      })
      .state('user-prefs', {
        url: '/help',
        template: '<div class="card-pf card-pf-accented card-pf-aggregate-status" style="height: 89px;">\
                          <div class="card-pf-body" style="height: 50px;">\
                            <p class="card-pf-aggregate-status-notifications">\
                              State: User Preferences\
                            </p>\
                          </div>\
                        </div>'
      })
      .state('logout', {
        url: '/help',
        template: '<div class="card-pf card-pf-accented card-pf-aggregate-status" style="height: 89px;">\
                          <div class="card-pf-body" style="height: 50px;">\
                            <p class="card-pf-aggregate-status-notifications">\
                              State: Logout\
                            </p>\
                          </div>\
                        </div>'
      });
  })
  .controller('vertNavWithRouterController', ['$scope',

    function ($scope) {
      $scope.navigationItems = [
        {
          title: "Dashboard",
          iconClass: "fa fa-dashboard",
          href: "#/dashboard"
        },
        {
          title: "Infrastructures",
          iconClass: "fa pficon-service",
          href: "#/iaas",
          badges: [
            {
              count: 83,
              tooltip: "Total number of items"
            }
          ]
        },
        {
          title: "Platforms",
          iconClass: "fa pficon-image",
          href: "#/paas",
          badges: [
            {
              count: 12,
              tooltip: "Total number of items"
            }
          ]
        },
        {
          title: "Settings",
          iconClass: "fa fa-paper-plane",
          children: [
            {
              title: "Credentials",
              href: "#/credentials",
              badges: [
                {
                  count: 2,
                  tooltip: "Total number of error items",
                  iconClass: 'pficon pficon-error-circle-o'
                },
                {
                  count: 6,
                  tooltip: "Total number warning error items",
                  iconClass: 'pficon pficon-warning-triangle-o'
                }
              ]
            },
            {
              title: "Secrets",
              href: "#/secrets",
              badges: [
                {
                  count: 9,
                  tooltip: "Total number of error items",
                  iconClass: 'pficon pficon-error-circle-o'
                }

              ]
            }
          ]
        },
        {
          title: "Admin",
          iconClass: "fa fa-map-marker",
          children: [
            {
              title: "Dashboard",
              href: "#/admin/dashboard",
              badges: []
            },
            {
              title: "Organizations",
              href: "#/admin/organizations",
              badges: []
            },

            {
              title: "Users",
              href: "#/admin/users",
              badges: []
            },

            {
              title: "IPAM",
              children: [
                {
                  title: "Prefixes",
                  href: "#/admin/ipam/prefixes",
                  badges: [
                    {
                      count: 6,
                      tooltip: "Total number of error items",
                      badgeClass: 'example-error-background'
                    }
                  ]
                },
                {
                  title: "Aggregates",
                  href: "#/admin/ipam/aggregates",
                  badges: [
                    {
                      count: 2,
                      tooltip: "Total number of items"
                    }
                  ]
                },
                {
                  title: "Virtual RF",
                  href: "#/admin/ipam/vrfs",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },
                {
                  title: "IP addresses",
                  href: "#/admin/ipam/ipaddresses",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },

                {
                  title: "Vlans",
                  href: "#/admin/ipam/vlans",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },

                {
                  title: "Internet Registries",
                  href: "#/admin/ipam/rirs",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },

                {
                  title: "Devices",
                  href: "#/admin/ipam/devices",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },

                {
                  title: "Virtual Machines",
                  href: "#/admin/ipam/virtualmachines",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },

                {
                  title: "Network Gears",
                  href: "#/amet/detracto/principes",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                },

                {
                  title: "Containers and Pods",
                  href: "#/admin/ipam/pods",
                  badges: [
                    {
                      count: 18,
                      tooltip: "Total number of warning items",
                      badgeClass: 'example-warning-background'
                    }
                  ]
                }

              ]
            },



            {
              title: "SDN",
              href: "#/admin/sdn",
              badges: []
            },

            {
              title: "Storages",
              href: "#/admin/storages",
              badges: []
            },

            {
              title: "Services",
              href: "#/admin/services",
              badges: []
            },


            {
              title: "Monitorings",
              href: "#/admin/monitorings",
              badges: []
            },

            {
              title: "Security",
              href: "#/admin/security",
              badges: []
            },

            {
              title: "PKI",
              href: "#/admin/pki",
              badges: []
            },

            {
              title: "Backups",
              href: "#/admin/backups",
              badges: []
            },

            {
              title: "Billings",
              href: "#/admin/billings",
              badges: []
            },

            {
              title: "Documentations",
              href: "#/admin/documentation",
              badges: []
            },

            {
              title: "Configs",
              href: "#/admin/configs",
              badges: []
            }
          ]
        },



        {
          title: "Help",
          iconClass: "fa pficon-help",
          href: "#/help",
          mobileOnly: true
        },
        {
          title: "User",
          iconClass: "fa pficon-user",
          mobileOnly: true,
          children: [
            { title: "User Preferences" },
            { title: "Logout" }
          ]
        }
      ];
    }
  ]);





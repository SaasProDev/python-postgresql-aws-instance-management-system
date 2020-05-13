import {
  ChangeDetectorRef,
  Component,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from './_services';
import { User, Token } from './_models';

import { VerticalNavigationItem } from 'patternfly-ng/navigation/vertical-navigation/vertical-navigation-item';

@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'app-root',
  styles: [`
    .faux-layout {
      position: fixed;
      top: 37px;
      bottom: 0;
      left: 0;
      right: 0;
      background-color: #f5f5f5;
      padding-top: 15px;
      z-index: 1100;
    }
    .example-page-container.container-fluid {
      position: fixed;
      top: 37px;
      bottom: 0;
      left: 0;
      right: 0;
      background-color: #f5f5f5;
      padding-top: 15px;
    }

    .hide-vertical-nav {
      margin-top: 15px;
      margin-left: 30px;
    }

    .navbar-brand-txt {
      line-height: 34px;
    }
  `],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {

  showExample: boolean = false;
  navigationItems: VerticalNavigationItem[];
  actionText: string = '';
  currentToken: Token;

  constructor(
    private chRef: ChangeDetectorRef,
    private authenticationService: AuthenticationService,
    private router: Router
  ) {

    this.authenticationService.currentToken.subscribe(x => this.currentToken = x);

  }

  logout() {
      this.authenticationService.logout();
      this.router.navigate(['/login']);
  }

  ngOnInit(): void {
    this.navigationItems = [
      {
        title: 'Logging',
        iconStyleClass: 'fa fa-list',
        url: '/instantlogging'
      },
      {
        title: 'Dashboard',
        iconStyleClass: 'fa fa-dashboard',
        url: '/terminal'
      },
      {
        title: 'Infrastructures',
        iconStyleClass: 'fa pficon-service',
        url: '/iaas',
        badges: [
          {
            count: 85,
            tooltip: 'Total number of items'
          }
        ]
      },
      {
        title: 'Platforms',
        iconStyleClass: 'fa pficon-image',
        badges: [
          {
            count: 15,
            tooltip: 'Total number of items'
          }
        ]
      },
      {
        title: 'Settings',
        iconStyleClass: 'fa fa-paper-plane',
        id: 'mySettings',
        children: [
          {
            title: "Credentials",
            url: "/credentials",
            badges: [],
            //   {
            //     count: 2,
            //     tooltip: "Total number of error items",
            //     iconStyleClass: 'pficon pficon-error-circle-o'
            //   },
            //   {
            //     count: 6,
            //     tooltip: "Total number warning error items",
            //     iconStyleClass: 'pficon pficon-warning-triangle-o'
            //   }
            // ]
          },
          {
            title: "Secrets",
            url: "/secrets",
            badges: [
              {
                count: 9,
                tooltip: "Total number of error items",
                iconStyleClass: 'pficon pficon-error-circle-o'
              }

            ]
          }
        ]
      },
      {
        title: "Admin",
        iconStyleClass: "fa fa-map-marker",
        children: [
          {
            title: "Dashboard",
            url: "/admin/dashboard",
            badges: []
          },
          {
            title: "Organizations",
            url: "/admin/organizations",
            badges: []
          },

          {
            title: "Users",
            url: "/admin/users",
            badges: []
          },

          {
            title: "IPAM",
            children: [
              {
                title: "Prefixes",
                url: "/admin/ipam/prefixes",
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
                url: "/admin/ipam/aggregates",
                badges: [
                  {
                    count: 2,
                    tooltip: "Total number of items"
                  }
                ]
              },
              {
                title: "Virtual RF",
                url: "/admin/ipam/vrfs",
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
                url: "/admin/ipam/ipaddresses",
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
                url: "/admin/ipam/vlans",
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
                url: "/admin/ipam/rirs",
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
                url: "/admin/ipam/devices",
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
                url: "/admin/ipam/virtualmachines",
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
                url: "/amet/detracto/principes",
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
                url: "/admin/ipam/pods",
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
            url: "/admin/sdn",
            badges: []
          },

          {
            title: "Storages",
            url: "/admin/storages",
            badges: []
          },

          {
            title: "Services",
            url: "/admin/services",
            badges: []
          },


          {
            title: "Monitorings",
            url: "/admin/monitorings",
            badges: []
          },

          {
            title: "Security",
            url: "/admin/security",
            badges: []
          },

          {
            title: "PKI",
            url: "/admin/pki",
            badges: []
          },

          {
            title: "Backups",
            url: "/admin/backups",
            badges: []
          },

          {
            title: "Billings",
            url: "/admin/billings",
            badges: []
          },

          {
            title: "Documentations",
            url: "/admin/documentation",
            badges: []
          },

          {
            title: "Configs",
            url: "/admin/configs",
            badges: []
          },

          {
            title: "Tools",
            url: "/admin/externaltools",
            badges: []
          },

        ]
      }
    ];
  }

  toggleExample(): void {
    this.showExample = !this.showExample;
    this.chRef.detectChanges();
  }

  onItemClicked($event: VerticalNavigationItem): void {
    this.actionText += 'Item Clicked: ' + $event.title + '\n';
  }

  onNavigation($event: VerticalNavigationItem): void {
    this.actionText += 'Navigation event fired: ' + $event.title + '\n';
  }
}


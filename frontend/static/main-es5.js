function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"], {
  /***/
  "./$$_lazy_route_resource lazy recursive":
  /*!******************************************************!*\
    !*** ./$$_lazy_route_resource lazy namespace object ***!
    \******************************************************/

  /*! no static exports found */

  /***/
  function $$_lazy_route_resourceLazyRecursive(module, exports) {
    function webpackEmptyAsyncContext(req) {
      // Here Promise.resolve().then() is used instead of new Promise() to prevent
      // uncaught exception popping up in devtools
      return Promise.resolve().then(function () {
        var e = new Error("Cannot find module '" + req + "'");
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      });
    }

    webpackEmptyAsyncContext.keys = function () {
      return [];
    };

    webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
    module.exports = webpackEmptyAsyncContext;
    webpackEmptyAsyncContext.id = "./$$_lazy_route_resource lazy recursive";
    /***/
  },

  /***/
  "./node_modules/raw-loader/dist/cjs.js!./src/app/ahome-term/ahome-term.component.html":
  /*!********************************************************************************************!*\
    !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/ahome-term/ahome-term.component.html ***!
    \********************************************************************************************/

  /*! exports provided: default */

  /***/
  function node_modulesRawLoaderDistCjsJsSrcAppAhomeTermAhomeTermComponentHtml(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "<p>ahome-term works!</p>\n<div id=\"terminal\"></div>";
    /***/
  },

  /***/
  "./node_modules/raw-loader/dist/cjs.js!./src/app/app.component.html":
  /*!**************************************************************************!*\
    !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/app.component.html ***!
    \**************************************************************************/

  /*! exports provided: default */

  /***/
  function node_modulesRawLoaderDistCjsJsSrcAppAppComponentHtml(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "<div id=\"verticalNavLayout\" class=\"layout-pf layout-pf-fixed faux-layout\" style=\"background-color: white;\" *ngIf=\"currentToken ; else loginUser\">\n  <pfng-vertical-navigation id=\"myNav\" [brandAlt]=\"'AHOME Enterprise Edition'\" [contentContainer]=\"contentContainer\"\n    [items]=\"navigationItems\"\n    [persistentSecondary]=\"false\"\n    [pinnableMenus]=\"true\"\n    [showBadges]=\"true\"\n    [showIcons]=\"true\"\n    [updateActiveItemsOnClick]=\"true\"\n    (onItemClickEvent)=\"onItemClicked($event)\"\n    (onNavigationEvent)=\"onNavigation($event)\">\n    <div>\n\n      <ul class=\"nav navbar-nav navbar-right navbar-iconic\">\n        <li class=\"dropdown\">\n        </li>\n        <li class=\"dropdown\" dropdown>\n          <a class=\"dropdown-toggle nav-item-iconic\" id=\"dropdownMenu1\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"true\" dropdownToggle>\n            <span title=\"Help\" class=\"fa pficon-help\"></span>\n            <span class=\"caret\"></span>\n          </a>\n          <ul class=\"dropdown-menu\" aria-labelledby=\"dropdownMenu1\" *dropdownMenu>\n            <li><a href=\"#\">Help</a></li>\n            <li><a href=\"#\">About</a></li>\n          </ul>\n        </li>\n        <li class=\"dropdown\" dropdown>\n          <a class=\"dropdown-toggle nav-item-iconic\" id=\"dropdownMenu2\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"true\" dropdownToggle>\n            <span title=\"Username\" class=\"fa pficon-user\"></span>\n            <span class=\"caret\"></span>\n          </a>\n          <ul class=\"dropdown-menu\" aria-labelledby=\"dropdownMenu2\" *dropdownMenu>\n            <li><a href=\"#\">Preferences</a></li>\n            <li><a href=\"#\">Logout</a></li>\n          </ul>\n        </li>\n      </ul>\n    </div>\n  </pfng-vertical-navigation>\n  <div #contentContainer\n    class=\"container-fluid container-cards-pf container-pf-nav-pf-vertical example-page-container nav-pf-vertical-with-badges\"\n    style=\"background-color: white;\">\n    <div class=\"row\">\n      <div class=\"col-sm-12\">\n        <h4 class=\"actions-label\">Actions...</h4>\n        <hr />\n      </div>\n    </div>\n    <div class=\"row\">\n      <div class=\"col-sm-12\">\n\n        <router-outlet></router-outlet>\n\n        <!-- nav -->\n        <nav class=\"navbar navbar-expand navbar-dark bg-dark\">\n            <div class=\"navbar-nav\">\n                <a class=\"nav-item nav-link\" routerLink=\"/\">Home</a>[ xxxx ]\n                <a class=\"nav-item nav-link\" (click)=\"logout()\">Logout</a>\n            </div>\n        </nav>\n        \n      </div>\n    </div>\n  </div>\n\n</div>\n\n<ng-template #loginUser>\n  <router-outlet></router-outlet>\n</ng-template>\n\n\n";
    /***/
  },

  /***/
  "./node_modules/raw-loader/dist/cjs.js!./src/app/home/home.component.html":
  /*!********************************************************************************!*\
    !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/home/home.component.html ***!
    \********************************************************************************/

  /*! exports provided: default */

  /***/
  function node_modulesRawLoaderDistCjsJsSrcAppHomeHomeComponentHtml(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "<div class=\"card mt-4\">\n    <h4 class=\"card-header\">You're logged in!!</h4>\n    <div class=\"card-body\">\n        <h6>Users from secure api end point</h6>\n        <div *ngIf=\"loading\" class=\"spinner-border spinner-border-sm\"></div>\n        <ul *ngIf=\"users\">\n            <li *ngFor=\"let user of users.results\">username: {{user.username}}</li>\n        </ul>\n    </div>\n</div>";
    /***/
  },

  /***/
  "./node_modules/raw-loader/dist/cjs.js!./src/app/iaas/iaas.component.html":
  /*!********************************************************************************!*\
    !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/iaas/iaas.component.html ***!
    \********************************************************************************/

  /*! exports provided: default */

  /***/
  function node_modulesRawLoaderDistCjsJsSrcAppIaasIaasComponentHtml(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "<!-- <div class=\"padding-15\">\n    <div class=\"row\">\n        <div class=\"col-sm-12\">\n            <div class=\"form-group\">\n                <pfng-list id=\"myList\" [actionTemplate]=\"actionTemplate\"\n                    [expandTemplate]=\"expandTemplate\" [items]=\"items\" [itemTemplate]=\"itemTemplate\"\n                    (onActionSelect)=\"handleAction($event, null)\" (onClick)=\"handleClick($event)\"\n                    (onDblClick)=\"handleDblClick($event)\" (onSelectionChange)=\"handleSelectionChange($event)\">\n                    <ng-template #itemTemplate let-item=\"item\" let-index=\"index\">\n                        <div class=\"list-pf-left\">\n                            <span\n                                class=\"fa {{item.typeIcon}} list-pf-icon list-pf-icon-bordered list-pf-icon-small\"></span>\n                        </div>\n                        <div class=\"list-pf-content-wrapper\">\n                            <div class=\"list-pf-main-content\">\n                                <div class=\"list-pf-title\">{{item.name}}</div>\n                                <div class=\"list-pf-description text-overflow-pf\">{{item.address}}</div>\n                            </div>\n                            <div class=\"list-pf-additional-content\">\n                                <div>\n                                    <span class=\"pficon pficon-screen\"></span>\n                                    <strong>{{item.hostCount}}</strong> Hosts\n                                </div>\n                                <div>\n                                    <span class=\"pficon pficon-cluster\"></span>\n                                    <strong>{{item.clusterCount}}</strong> Clusters\n                                </div>\n                                <div>\n                                    <span class=\"pficon pficon-container-node\"></span>\n                                    <strong>{{item.nodeCount}}</strong> Nodes\n                                </div>\n                                <div>\n                                    <span class=\"pficon pficon-image\"></span>\n                                    <strong>{{item.imageCount}}</strong> Images\n                                </div>\n                            </div>\n                        </div>\n                    </ng-template>\n                    <ng-template #actionTemplate let-item=\"item\" let-index=\"index\">\n                        <pfng-action class=\"list-pf-actions\"\n                            [config]=\"getActionConfig(item, actionButtonTemplate, startButtonTemplate)\"\n                            (onActionSelect)=\"handleAction($event, item)\">\n                            <ng-template #actionButtonTemplate let-action=\"action\">\n                                <span class=\"fa fa-plus\">&nbsp;</span>{{action.title}}\n                            </ng-template>\n                            <ng-template #startButtonTemplate let-action=\"action\">\n                                {{item.started === true ? \"Starting\" : action.title}}\n                            </ng-template>\n                        </pfng-action>\n                    </ng-template>\n                    <ng-template #expandTemplate let-item=\"item\" let-index=\"index\">\n                        <basic-content [item]=\"item\"></basic-content>\n                    </ng-template>\n                </pfng-list>\n            </div>\n        </div>\n    </div>\n</div>\n-->\n<h1>Iaas Page</h1>\n<div style=\"text-align:center\">\n    <div [innerHtml]=\"htmlSnippet\"></div>\n</div>";
    /***/
  },

  /***/
  "./node_modules/raw-loader/dist/cjs.js!./src/app/login/login.component.html":
  /*!**********************************************************************************!*\
    !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/login/login.component.html ***!
    \**********************************************************************************/

  /*! exports provided: default */

  /***/
  function node_modulesRawLoaderDistCjsJsSrcAppLoginLoginComponentHtml(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "<div class=\"col-md-6 offset-md-3 mt-5\">\n    <div class=\"alert alert-info\">\n        Username: test<br />\n        Password: test\n    </div>\n    <div class=\"card\">\n        <h4 class=\"card-header\">Login</h4>\n        <div class=\"card-body\">\n            <form [formGroup]=\"loginForm\" (ngSubmit)=\"onSubmit()\">\n                <div class=\"form-group\">\n                    <label for=\"username\">Username</label>\n                    <input type=\"text\" formControlName=\"username\" class=\"form-control\" [ngClass]=\"{ 'is-invalid': submitted && f.username.errors }\" />\n                    <div *ngIf=\"submitted && f.username.errors\" class=\"invalid-feedback\">\n                        <div *ngIf=\"f.username.errors.required\">Username is required</div>\n                    </div>\n                </div>\n                <div class=\"form-group\">\n                    <label for=\"password\">Password</label>\n                    <input type=\"password\" formControlName=\"password\" class=\"form-control\" [ngClass]=\"{ 'is-invalid': submitted && f.password.errors }\" />\n                    <div *ngIf=\"submitted && f.password.errors\" class=\"invalid-feedback\">\n                        <div *ngIf=\"f.password.errors.required\">Password is required</div>\n                    </div>\n                </div>\n                <button [disabled]=\"loading\" class=\"btn btn-primary\">\n                    <span *ngIf=\"loading\" class=\"spinner-border spinner-border-sm mr-1\"></span>\n                    Login\n                </button>\n                <div *ngIf=\"error\" class=\"alert alert-danger mt-3 mb-0\">{{error}}</div>\n            </form>\n        </div>\n    </div>\n</div>";
    /***/
  },

  /***/
  "./node_modules/tslib/tslib.es6.js":
  /*!*****************************************!*\
    !*** ./node_modules/tslib/tslib.es6.js ***!
    \*****************************************/

  /*! exports provided: __extends, __assign, __rest, __decorate, __param, __metadata, __awaiter, __generator, __exportStar, __values, __read, __spread, __spreadArrays, __await, __asyncGenerator, __asyncDelegator, __asyncValues, __makeTemplateObject, __importStar, __importDefault */

  /***/
  function node_modulesTslibTslibEs6Js(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__extends", function () {
      return __extends;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__assign", function () {
      return _assign;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__rest", function () {
      return __rest;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__decorate", function () {
      return __decorate;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__param", function () {
      return __param;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__metadata", function () {
      return __metadata;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__awaiter", function () {
      return __awaiter;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__generator", function () {
      return __generator;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__exportStar", function () {
      return __exportStar;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__values", function () {
      return __values;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__read", function () {
      return __read;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__spread", function () {
      return __spread;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__spreadArrays", function () {
      return __spreadArrays;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__await", function () {
      return __await;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__asyncGenerator", function () {
      return __asyncGenerator;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__asyncDelegator", function () {
      return __asyncDelegator;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__asyncValues", function () {
      return __asyncValues;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__makeTemplateObject", function () {
      return __makeTemplateObject;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__importStar", function () {
      return __importStar;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "__importDefault", function () {
      return __importDefault;
    });
    /*! *****************************************************************************
    Copyright (c) Microsoft Corporation. All rights reserved.
    Licensed under the Apache License, Version 2.0 (the "License"); you may not use
    this file except in compliance with the License. You may obtain a copy of the
    License at http://www.apache.org/licenses/LICENSE-2.0
    
    THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
    WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
    MERCHANTABLITY OR NON-INFRINGEMENT.
    
    See the Apache Version 2.0 License for specific language governing permissions
    and limitations under the License.
    ***************************************************************************** */

    /* global Reflect, Promise */


    var _extendStatics = function extendStatics(d, b) {
      _extendStatics = Object.setPrototypeOf || {
        __proto__: []
      } instanceof Array && function (d, b) {
        d.__proto__ = b;
      } || function (d, b) {
        for (var p in b) {
          if (b.hasOwnProperty(p)) d[p] = b[p];
        }
      };

      return _extendStatics(d, b);
    };

    function __extends(d, b) {
      _extendStatics(d, b);

      function __() {
        this.constructor = d;
      }

      d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    }

    var _assign = function __assign() {
      _assign = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
          s = arguments[i];

          for (var p in s) {
            if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
          }
        }

        return t;
      };

      return _assign.apply(this, arguments);
    };

    function __rest(s, e) {
      var t = {};

      for (var p in s) {
        if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0) t[p] = s[p];
      }

      if (s != null && typeof Object.getOwnPropertySymbols === "function") for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
        if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i])) t[p[i]] = s[p[i]];
      }
      return t;
    }

    function __decorate(decorators, target, key, desc) {
      var c = arguments.length,
          r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc,
          d;
      if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);else for (var i = decorators.length - 1; i >= 0; i--) {
        if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
      }
      return c > 3 && r && Object.defineProperty(target, key, r), r;
    }

    function __param(paramIndex, decorator) {
      return function (target, key) {
        decorator(target, key, paramIndex);
      };
    }

    function __metadata(metadataKey, metadataValue) {
      if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(metadataKey, metadataValue);
    }

    function __awaiter(thisArg, _arguments, P, generator) {
      return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) {
          try {
            step(generator.next(value));
          } catch (e) {
            reject(e);
          }
        }

        function rejected(value) {
          try {
            step(generator["throw"](value));
          } catch (e) {
            reject(e);
          }
        }

        function step(result) {
          result.done ? resolve(result.value) : new P(function (resolve) {
            resolve(result.value);
          }).then(fulfilled, rejected);
        }

        step((generator = generator.apply(thisArg, _arguments || [])).next());
      });
    }

    function __generator(thisArg, body) {
      var _ = {
        label: 0,
        sent: function sent() {
          if (t[0] & 1) throw t[1];
          return t[1];
        },
        trys: [],
        ops: []
      },
          f,
          y,
          t,
          g;
      return g = {
        next: verb(0),
        "throw": verb(1),
        "return": verb(2)
      }, typeof Symbol === "function" && (g[Symbol.iterator] = function () {
        return this;
      }), g;

      function verb(n) {
        return function (v) {
          return step([n, v]);
        };
      }

      function step(op) {
        if (f) throw new TypeError("Generator is already executing.");

        while (_) {
          try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];

            switch (op[0]) {
              case 0:
              case 1:
                t = op;
                break;

              case 4:
                _.label++;
                return {
                  value: op[1],
                  done: false
                };

              case 5:
                _.label++;
                y = op[1];
                op = [0];
                continue;

              case 7:
                op = _.ops.pop();

                _.trys.pop();

                continue;

              default:
                if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) {
                  _ = 0;
                  continue;
                }

                if (op[0] === 3 && (!t || op[1] > t[0] && op[1] < t[3])) {
                  _.label = op[1];
                  break;
                }

                if (op[0] === 6 && _.label < t[1]) {
                  _.label = t[1];
                  t = op;
                  break;
                }

                if (t && _.label < t[2]) {
                  _.label = t[2];

                  _.ops.push(op);

                  break;
                }

                if (t[2]) _.ops.pop();

                _.trys.pop();

                continue;
            }

            op = body.call(thisArg, _);
          } catch (e) {
            op = [6, e];
            y = 0;
          } finally {
            f = t = 0;
          }
        }

        if (op[0] & 5) throw op[1];
        return {
          value: op[0] ? op[1] : void 0,
          done: true
        };
      }
    }

    function __exportStar(m, exports) {
      for (var p in m) {
        if (!exports.hasOwnProperty(p)) exports[p] = m[p];
      }
    }

    function __values(o) {
      var m = typeof Symbol === "function" && o[Symbol.iterator],
          i = 0;
      if (m) return m.call(o);
      return {
        next: function next() {
          if (o && i >= o.length) o = void 0;
          return {
            value: o && o[i++],
            done: !o
          };
        }
      };
    }

    function __read(o, n) {
      var m = typeof Symbol === "function" && o[Symbol.iterator];
      if (!m) return o;
      var i = m.call(o),
          r,
          ar = [],
          e;

      try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) {
          ar.push(r.value);
        }
      } catch (error) {
        e = {
          error: error
        };
      } finally {
        try {
          if (r && !r.done && (m = i["return"])) m.call(i);
        } finally {
          if (e) throw e.error;
        }
      }

      return ar;
    }

    function __spread() {
      for (var ar = [], i = 0; i < arguments.length; i++) {
        ar = ar.concat(__read(arguments[i]));
      }

      return ar;
    }

    function __spreadArrays() {
      for (var s = 0, i = 0, il = arguments.length; i < il; i++) {
        s += arguments[i].length;
      }

      for (var r = Array(s), k = 0, i = 0; i < il; i++) {
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++) {
          r[k] = a[j];
        }
      }

      return r;
    }

    ;

    function __await(v) {
      return this instanceof __await ? (this.v = v, this) : new __await(v);
    }

    function __asyncGenerator(thisArg, _arguments, generator) {
      if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
      var g = generator.apply(thisArg, _arguments || []),
          i,
          q = [];
      return i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () {
        return this;
      }, i;

      function verb(n) {
        if (g[n]) i[n] = function (v) {
          return new Promise(function (a, b) {
            q.push([n, v, a, b]) > 1 || resume(n, v);
          });
        };
      }

      function resume(n, v) {
        try {
          step(g[n](v));
        } catch (e) {
          settle(q[0][3], e);
        }
      }

      function step(r) {
        r.value instanceof __await ? Promise.resolve(r.value.v).then(fulfill, reject) : settle(q[0][2], r);
      }

      function fulfill(value) {
        resume("next", value);
      }

      function reject(value) {
        resume("throw", value);
      }

      function settle(f, v) {
        if (f(v), q.shift(), q.length) resume(q[0][0], q[0][1]);
      }
    }

    function __asyncDelegator(o) {
      var i, p;
      return i = {}, verb("next"), verb("throw", function (e) {
        throw e;
      }), verb("return"), i[Symbol.iterator] = function () {
        return this;
      }, i;

      function verb(n, f) {
        i[n] = o[n] ? function (v) {
          return (p = !p) ? {
            value: __await(o[n](v)),
            done: n === "return"
          } : f ? f(v) : v;
        } : f;
      }
    }

    function __asyncValues(o) {
      if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
      var m = o[Symbol.asyncIterator],
          i;
      return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () {
        return this;
      }, i);

      function verb(n) {
        i[n] = o[n] && function (v) {
          return new Promise(function (resolve, reject) {
            v = o[n](v), settle(resolve, reject, v.done, v.value);
          });
        };
      }

      function settle(resolve, reject, d, v) {
        Promise.resolve(v).then(function (v) {
          resolve({
            value: v,
            done: d
          });
        }, reject);
      }
    }

    function __makeTemplateObject(cooked, raw) {
      if (Object.defineProperty) {
        Object.defineProperty(cooked, "raw", {
          value: raw
        });
      } else {
        cooked.raw = raw;
      }

      return cooked;
    }

    ;

    function __importStar(mod) {
      if (mod && mod.__esModule) return mod;
      var result = {};
      if (mod != null) for (var k in mod) {
        if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
      }
      result.default = mod;
      return result;
    }

    function __importDefault(mod) {
      return mod && mod.__esModule ? mod : {
        default: mod
      };
    }
    /***/

  },

  /***/
  "./src/app/_helpers/auth.guard.ts":
  /*!****************************************!*\
    !*** ./src/app/_helpers/auth.guard.ts ***!
    \****************************************/

  /*! exports provided: AuthGuard */

  /***/
  function srcApp_helpersAuthGuardTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "AuthGuard", function () {
      return AuthGuard;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/router */
    "./node_modules/@angular/router/fesm2015/router.js");
    /* harmony import */


    var _app_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @app/_services */
    "./src/app/_services/index.ts");

    var AuthGuard =
    /*#__PURE__*/
    function () {
      function AuthGuard(router, authenticationService) {
        _classCallCheck(this, AuthGuard);

        this.router = router;
        this.authenticationService = authenticationService;
      }

      _createClass(AuthGuard, [{
        key: "canActivate",
        value: function canActivate(route, state) {
          var currentToken = this.authenticationService.currentTokenValue;

          if (currentToken) {
            // logged in so return true
            return true;
          } // not logged in so redirect to login page with the return url


          this.router.navigate(['/login'], {
            queryParams: {
              returnUrl: state.url
            }
          });
          return false;
        }
      }]);

      return AuthGuard;
    }();

    AuthGuard.ctorParameters = function () {
      return [{
        type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]
      }, {
        type: _app_services__WEBPACK_IMPORTED_MODULE_3__["AuthenticationService"]
      }];
    };

    AuthGuard = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
      providedIn: 'root'
    })], AuthGuard);
    /***/
  },

  /***/
  "./src/app/_helpers/error.interceptor.ts":
  /*!***********************************************!*\
    !*** ./src/app/_helpers/error.interceptor.ts ***!
    \***********************************************/

  /*! exports provided: ErrorInterceptor */

  /***/
  function srcApp_helpersErrorInterceptorTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "ErrorInterceptor", function () {
      return ErrorInterceptor;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! rxjs */
    "./node_modules/rxjs/_esm2015/index.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _app_services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! @app/_services */
    "./src/app/_services/index.ts");

    var ErrorInterceptor =
    /*#__PURE__*/
    function () {
      function ErrorInterceptor(authenticationService) {
        _classCallCheck(this, ErrorInterceptor);

        this.authenticationService = authenticationService;
      }

      _createClass(ErrorInterceptor, [{
        key: "intercept",
        value: function intercept(request, next) {
          var _this = this;

          return next.handle(request).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function (err) {
            if (err.status === 401) {
              // auto logout if 401 response returned from api
              _this.authenticationService.logout(); // location.reload(true);

            }

            var error = err.error.message || err.statusText;
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["throwError"])(error);
          }));
        }
      }]);

      return ErrorInterceptor;
    }();

    ErrorInterceptor.ctorParameters = function () {
      return [{
        type: _app_services__WEBPACK_IMPORTED_MODULE_4__["AuthenticationService"]
      }];
    };

    ErrorInterceptor = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()], ErrorInterceptor);
    /***/
  },

  /***/
  "./src/app/_helpers/fake-backend.ts":
  /*!******************************************!*\
    !*** ./src/app/_helpers/fake-backend.ts ***!
    \******************************************/

  /*! exports provided: FakeBackendInterceptor, fakeBackendProvider */

  /***/
  function srcApp_helpersFakeBackendTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "FakeBackendInterceptor", function () {
      return FakeBackendInterceptor;
    });
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "fakeBackendProvider", function () {
      return fakeBackendProvider;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/fesm2015/http.js");
    /* harmony import */


    var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! rxjs */
    "./node_modules/rxjs/_esm2015/index.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");

    var users = [{
      id: 1,
      username: 'test',
      password: 'test',
      firstName: 'Test',
      lastName: 'User'
    }];

    var FakeBackendInterceptor =
    /*#__PURE__*/
    function () {
      function FakeBackendInterceptor() {
        _classCallCheck(this, FakeBackendInterceptor);
      }

      _createClass(FakeBackendInterceptor, [{
        key: "intercept",
        value: function intercept(request, next) {
          var url = request.url,
              method = request.method,
              headers = request.headers,
              body = request.body; // wrap in delayed observable to simulate server api call

          return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(null).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["mergeMap"])(handleRoute)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["materialize"])()) // call materialize and dematerialize to ensure delay even if an error is thrown (https://github.com/Reactive-Extensions/RxJS/issues/648)
          .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["delay"])(500)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["dematerialize"])());

          function handleRoute() {
            switch (true) {
              case url.endsWith('/users/authenticate') && method === 'POST':
                return authenticate();

              case url.endsWith('/users') && method === 'GET':
                return getUsers();

              default:
                // pass through any requests not handled above
                return next.handle(request);
            }
          } // route functions


          function authenticate() {
            var username = body.username,
                password = body.password;
            var user = users.find(function (x) {
              return x.username === username && x.password === password;
            });
            if (!user) return error('Username or password is incorrect');
            return ok({
              id: user.id,
              username: user.username,
              firstName: user.firstName,
              lastName: user.lastName,
              token: 'fake-jwt-token'
            });
          }

          function getUsers() {
            if (!isLoggedIn()) return unauthorized();
            return ok(users);
          } // helper functions


          function ok(body) {
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpResponse"]({
              status: 200,
              body: body
            }));
          }

          function error(message) {
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["throwError"])({
              error: {
                message: message
              }
            });
          }

          function unauthorized() {
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["throwError"])({
              status: 401,
              error: {
                message: 'Unauthorised'
              }
            });
          }

          function isLoggedIn() {
            return headers.get('Authorization') === 'Bearer fake-jwt-token';
          }
        }
      }]);

      return FakeBackendInterceptor;
    }();

    FakeBackendInterceptor = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()], FakeBackendInterceptor);
    var fakeBackendProvider = {
      // use fake backend in place of Http service for backend-less development
      provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HTTP_INTERCEPTORS"],
      useClass: FakeBackendInterceptor,
      multi: true
    };
    /***/
  },

  /***/
  "./src/app/_helpers/index.ts":
  /*!***********************************!*\
    !*** ./src/app/_helpers/index.ts ***!
    \***********************************/

  /*! exports provided: AuthGuard, ErrorInterceptor, FakeBackendInterceptor, fakeBackendProvider, JwtInterceptor */

  /***/
  function srcApp_helpersIndexTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _auth_guard__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! ./auth.guard */
    "./src/app/_helpers/auth.guard.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "AuthGuard", function () {
      return _auth_guard__WEBPACK_IMPORTED_MODULE_1__["AuthGuard"];
    });
    /* harmony import */


    var _error_interceptor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./error.interceptor */
    "./src/app/_helpers/error.interceptor.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "ErrorInterceptor", function () {
      return _error_interceptor__WEBPACK_IMPORTED_MODULE_2__["ErrorInterceptor"];
    });
    /* harmony import */


    var _fake_backend__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./fake-backend */
    "./src/app/_helpers/fake-backend.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "FakeBackendInterceptor", function () {
      return _fake_backend__WEBPACK_IMPORTED_MODULE_3__["FakeBackendInterceptor"];
    });
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "fakeBackendProvider", function () {
      return _fake_backend__WEBPACK_IMPORTED_MODULE_3__["fakeBackendProvider"];
    });
    /* harmony import */


    var _jwt_interceptor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ./jwt.interceptor */
    "./src/app/_helpers/jwt.interceptor.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "JwtInterceptor", function () {
      return _jwt_interceptor__WEBPACK_IMPORTED_MODULE_4__["JwtInterceptor"];
    });
    /***/

  },

  /***/
  "./src/app/_helpers/jwt.interceptor.ts":
  /*!*********************************************!*\
    !*** ./src/app/_helpers/jwt.interceptor.ts ***!
    \*********************************************/

  /*! exports provided: JwtInterceptor */

  /***/
  function srcApp_helpersJwtInterceptorTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "JwtInterceptor", function () {
      return JwtInterceptor;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _app_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @app/_services */
    "./src/app/_services/index.ts");

    var JwtInterceptor =
    /*#__PURE__*/
    function () {
      function JwtInterceptor(authenticationService) {
        _classCallCheck(this, JwtInterceptor);

        this.authenticationService = authenticationService;
      }

      _createClass(JwtInterceptor, [{
        key: "intercept",
        value: function intercept(request, next) {
          // add authorization header with jwt token if available
          var currentToken = this.authenticationService.currentTokenValue;

          if (currentToken && "".concat(currentToken.access)) {
            // console.log('Bearer: ' + `${currentToken.access}`);
            request = request.clone({
              setHeaders: {
                Authorization: "Bearer ".concat(currentToken.access)
              }
            });
          }

          return next.handle(request);
        }
      }]);

      return JwtInterceptor;
    }();

    JwtInterceptor.ctorParameters = function () {
      return [{
        type: _app_services__WEBPACK_IMPORTED_MODULE_2__["AuthenticationService"]
      }];
    };

    JwtInterceptor = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()], JwtInterceptor);
    /***/
  },

  /***/
  "./src/app/_services/authentication.service.ts":
  /*!*****************************************************!*\
    !*** ./src/app/_services/authentication.service.ts ***!
    \*****************************************************/

  /*! exports provided: AuthenticationService */

  /***/
  function srcApp_servicesAuthenticationServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "AuthenticationService", function () {
      return AuthenticationService;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/fesm2015/http.js");
    /* harmony import */


    var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! rxjs */
    "./node_modules/rxjs/_esm2015/index.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @environments/environment */
    "./src/environments/environment.ts");

    var AuthenticationService =
    /*#__PURE__*/
    function () {
      function AuthenticationService(http) {
        _classCallCheck(this, AuthenticationService);

        this.http = http;
        this.currentTokenSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](JSON.parse(localStorage.getItem('access_token')));
        this.currentToken = this.currentTokenSubject.asObservable();
      }

      _createClass(AuthenticationService, [{
        key: "login",
        value: function login(username, password) {
          var _this2 = this;

          return this.http.post("".concat(_environments_environment__WEBPACK_IMPORTED_MODULE_5__["environment"].apiUrl, "/api/token/"), {
            username: username,
            password: password
          }) // store user details and jwt token in local storage to keep user logged in between page refreshesh
          .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (res) {
            res.username = username;
            localStorage.setItem('access_token', JSON.stringify(res)); // console.log(JSON.stringify(res));

            _this2.currentTokenSubject.next(res);

            return res;
          }));
        }
      }, {
        key: "logout",
        value: function logout() {
          // remove user from local storage to log user out
          localStorage.removeItem('access_token');
          this.currentTokenSubject.next(null);
        }
      }, {
        key: "currentTokenValue",
        get: function get() {
          return this.currentTokenSubject.value;
        }
      }]);

      return AuthenticationService;
    }();

    AuthenticationService.ctorParameters = function () {
      return [{
        type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]
      }];
    };

    AuthenticationService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
      providedIn: 'root'
    })], AuthenticationService); // export class AuthService {
    //   endpoint: string = 'http://localhost:4000/api';
    //   headers = new HttpHeaders().set('Content-Type', 'application/json');
    //   currentUser = {};
    //   constructor(
    //     private http: HttpClient,
    //     public router: Router
    //   ) {
    //   }
    //   // Sign-up
    //   signUp(user: User): Observable<any> {
    //     let api = `${this.endpoint}/register-user`;
    //     return this.http.post(api, user)
    //       .pipe(
    //         catchError(this.handleError)
    //       )
    //   }
    //   // Sign-in
    //   signIn(user: User) {
    //     return this.http.post<any>(`${this.endpoint}/signin`, user)
    //       .subscribe((res: any) => {
    //         localStorage.setItem('access_token', res.token)
    //         this.getUserProfile(res._id).subscribe((res) => {
    //           this.currentUser = res;
    //           this.router.navigate(['user-profile/' + res.msg._id]);
    //         })
    //       })
    //   }
    //   getToken() {
    //     return localStorage.getItem('access_token');
    //   }
    //   get isLoggedIn(): boolean {
    //     let authToken = localStorage.getItem('access_token');
    //     return (authToken !== null) ? true : false;
    //   }
    //   doLogout() {
    //     let removeToken = localStorage.removeItem('access_token');
    //     if (removeToken == null) {
    //       this.router.navigate(['log-in']);
    //     }
    //   }
    //   // User profile
    //   getUserProfile(id): Observable<any> {
    //     let api = `${this.endpoint}/user-profile/${id}`;
    //     return this.http.get(api, { headers: this.headers }).pipe(
    //       map((res: Response) => {
    //         return res || {}
    //       }),
    //       catchError(this.handleError)
    //     )
    //   }
    //   // Error 
    //   handleError(error: HttpErrorResponse) {
    //     let msg = '';
    //     if (error.error instanceof ErrorEvent) {
    //       // client-side error
    //       msg = error.error.message;
    //     } else {
    //       // server-side error
    //       msg = `Error Code: ${error.status}\nMessage: ${error.message}`;
    //     }
    //     return throwError(msg);
    //   }
    // }

    /***/
  },

  /***/
  "./src/app/_services/frontend.service.ts":
  /*!***********************************************!*\
    !*** ./src/app/_services/frontend.service.ts ***!
    \***********************************************/

  /*! exports provided: FrontendService */

  /***/
  function srcApp_servicesFrontendServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "FrontendService", function () {
      return FrontendService;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/fesm2015/http.js");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! @environments/environment */
    "./src/environments/environment.ts");

    var httpOptions = {
      headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_3__["HttpHeaders"]({
        'Content-Type': 'text/html',
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      })
    };

    var FrontendService =
    /*#__PURE__*/
    function () {
      function FrontendService(http) {
        _classCallCheck(this, FrontendService);

        this.http = http; // headers = new HttpHeaders().set('Content-Type', 'application/json');

        this.headers = new _angular_common_http__WEBPACK_IMPORTED_MODULE_3__["HttpHeaders"]().set('Content-Type', 'text/html');
        this.htmlSnippet = '';
        this.token = localStorage.getItem('access_token');
      }

      _createClass(FrontendService, [{
        key: "getIaas",
        value: function getIaas() {
          var options = {
            headers: {
              'Authorization': 'Bearer ' + this.token
            },
            responseType: 'text'
          }; // return this.http.get(`${environment.apiUrl}/frontend/organizations/list/`, { headers: {'Accept': 'text/html', 'Content-Type': 'text/html', 'Authorization': 'Bearer '+localStorage.getItem('access_token')} });

          var url = "".concat(_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].apiUrl, "/frontend/organizations/list/"); // console.log(url);
          // console.log( localStorage.getItem('access_token') );

          return this.http.get(url, {
            responseType: 'text',
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])( // Log the result or error
          // Log the result or error
          function (data) {
            data;
          })); // this.http.get(url, {responseType: 'text'})
          //     .subscribe(
          //         data => { 
          //         	// console.log(data);
          //         	this.htmlSnippet = data; 
          //         }
          //     );
          // return this.htmlSnippet;
          //   return this.http.get(url, {responseType: 'text'}).subscribe(data => {
          // 	  console.log(data);
          // 	  return data;
          // });
          // return this.http.get( url, {responseType: 'text', headers :{'Accept': 'text/html', 'Authorization': 'Bearer '+localStorage.getItem('access_token')}} );
          // return this.http.get(url, {responseType: 'text'})
          //     .pipe(
          //       tap( // Log the result or error
          //         data => data
          //       )
          //     );
          // return this.http.get('...', { responseType: 'text' }); 
        }
      }]);

      return FrontendService;
    }();

    FrontendService.ctorParameters = function () {
      return [{
        type: _angular_common_http__WEBPACK_IMPORTED_MODULE_3__["HttpClient"]
      }];
    };

    FrontendService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
      providedIn: 'root'
    })], FrontendService);
    /***/
  },

  /***/
  "./src/app/_services/index.ts":
  /*!************************************!*\
    !*** ./src/app/_services/index.ts ***!
    \************************************/

  /*! exports provided: AuthenticationService, UserService, FrontendService */

  /***/
  function srcApp_servicesIndexTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _authentication_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! ./authentication.service */
    "./src/app/_services/authentication.service.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "AuthenticationService", function () {
      return _authentication_service__WEBPACK_IMPORTED_MODULE_1__["AuthenticationService"];
    });
    /* harmony import */


    var _user_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./user.service */
    "./src/app/_services/user.service.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "UserService", function () {
      return _user_service__WEBPACK_IMPORTED_MODULE_2__["UserService"];
    });
    /* harmony import */


    var _frontend_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./frontend.service */
    "./src/app/_services/frontend.service.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "FrontendService", function () {
      return _frontend_service__WEBPACK_IMPORTED_MODULE_3__["FrontendService"];
    });
    /***/

  },

  /***/
  "./src/app/_services/user.service.ts":
  /*!*******************************************!*\
    !*** ./src/app/_services/user.service.ts ***!
    \*******************************************/

  /*! exports provided: UserService */

  /***/
  function srcApp_servicesUserServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "UserService", function () {
      return UserService;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/fesm2015/http.js");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @environments/environment */
    "./src/environments/environment.ts");

    var UserService =
    /*#__PURE__*/
    function () {
      function UserService(http) {
        _classCallCheck(this, UserService);

        this.http = http;
      }

      _createClass(UserService, [{
        key: "getAll",
        value: function getAll() {
          return this.http.get("".concat(_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].apiUrl, "/api/v1/users/"));
        }
      }]);

      return UserService;
    }();

    UserService.ctorParameters = function () {
      return [{
        type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]
      }];
    };

    UserService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
      providedIn: 'root'
    })], UserService);
    /***/
  },

  /***/
  "./src/app/ahome-term/ahome-term.component.css":
  /*!*****************************************************!*\
    !*** ./src/app/ahome-term/ahome-term.component.css ***!
    \*****************************************************/

  /*! exports provided: default */

  /***/
  function srcAppAhomeTermAhomeTermComponentCss(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "";
    /***/
  },

  /***/
  "./src/app/ahome-term/ahome-term.component.ts":
  /*!****************************************************!*\
    !*** ./src/app/ahome-term/ahome-term.component.ts ***!
    \****************************************************/

  /*! exports provided: AhomeTermComponent */

  /***/
  function srcAppAhomeTermAhomeTermComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "AhomeTermComponent", function () {
      return AhomeTermComponent;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var xterm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! xterm */
    "../node_modules/xterm/lib/xterm.js");
    /* harmony import */


    var xterm__WEBPACK_IMPORTED_MODULE_2___default =
    /*#__PURE__*/
    __webpack_require__.n(xterm__WEBPACK_IMPORTED_MODULE_2__);
    /* harmony import */


    var xterm_addon_fit__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! xterm-addon-fit */
    "../node_modules/xterm-addon-fit/lib/xterm-addon-fit.js");
    /* harmony import */


    var xterm_addon_fit__WEBPACK_IMPORTED_MODULE_3___default =
    /*#__PURE__*/
    __webpack_require__.n(xterm_addon_fit__WEBPACK_IMPORTED_MODULE_3__);
    /* harmony import */


    var _services_socketio_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../services/socketio.service */
    "./src/app/services/socketio.service.ts"); // socketio


    var AhomeTermComponent =
    /*#__PURE__*/
    function () {
      function AhomeTermComponent(socketioService) {
        _classCallCheck(this, AhomeTermComponent);
      }

      _createClass(AhomeTermComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          this.terminal = new xterm__WEBPACK_IMPORTED_MODULE_2__["Terminal"]({
            cursorBlink: true
          });
          var fitAddon = new xterm_addon_fit__WEBPACK_IMPORTED_MODULE_3__["FitAddon"]();
          this.terminal.loadAddon(fitAddon);
          this.container = document.getElementById('terminal');
          this.terminal.open(this.container);
          fitAddon.fit();
          this.terminal.write('Welcome to xterm.js !!!');
        }
      }]);

      return AhomeTermComponent;
    }();

    AhomeTermComponent.ctorParameters = function () {
      return [{
        type: _services_socketio_service__WEBPACK_IMPORTED_MODULE_4__["SocketioService"]
      }];
    };

    AhomeTermComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
      selector: 'app-ahome-term',
      template: tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! raw-loader!./ahome-term.component.html */
      "./node_modules/raw-loader/dist/cjs.js!./src/app/ahome-term/ahome-term.component.html")).default,
      encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewEncapsulation"].None,
      styles: [tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! ./ahome-term.component.css */
      "./src/app/ahome-term/ahome-term.component.css")).default]
    })], AhomeTermComponent);
    /***/
  },

  /***/
  "./src/app/app-routing.module.ts":
  /*!***************************************!*\
    !*** ./src/app/app-routing.module.ts ***!
    \***************************************/

  /*! exports provided: AppRoutingModule */

  /***/
  function srcAppAppRoutingModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function () {
      return AppRoutingModule;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/router */
    "./node_modules/@angular/router/fesm2015/router.js");
    /* harmony import */


    var _ahome_term_ahome_term_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./ahome-term/ahome-term.component */
    "./src/app/ahome-term/ahome-term.component.ts");
    /* harmony import */


    var _iaas_iaas_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ./iaas/iaas.component */
    "./src/app/iaas/iaas.component.ts");
    /* harmony import */


    var _home__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! ./home */
    "./src/app/home/index.ts");
    /* harmony import */


    var _login__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ./login */
    "./src/app/login/index.ts");
    /* harmony import */


    var _helpers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! ./_helpers */
    "./src/app/_helpers/index.ts");

    var routes = [{
      path: '',
      component: _home__WEBPACK_IMPORTED_MODULE_5__["HomeComponent"],
      canActivate: [_helpers__WEBPACK_IMPORTED_MODULE_7__["AuthGuard"]]
    }, {
      path: 'login',
      component: _login__WEBPACK_IMPORTED_MODULE_6__["LoginComponent"]
    }, {
      path: "terminal",
      component: _ahome_term_ahome_term_component__WEBPACK_IMPORTED_MODULE_3__["AhomeTermComponent"]
    }, {
      path: "iaas",
      component: _iaas_iaas_component__WEBPACK_IMPORTED_MODULE_4__["IaasComponent"]
    }, // otherwise redirect to home
    {
      path: '**',
      redirectTo: ''
    }];

    var AppRoutingModule = function AppRoutingModule() {
      _classCallCheck(this, AppRoutingModule);
    };

    AppRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
      imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forRoot(routes, {
        useHash: true
      })],
      exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
    })], AppRoutingModule);
    /***/
  },

  /***/
  "./src/app/app.component.ts":
  /*!**********************************!*\
    !*** ./src/app/app.component.ts ***!
    \**********************************/

  /*! exports provided: AppComponent */

  /***/
  function srcAppAppComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "AppComponent", function () {
      return AppComponent;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/router */
    "./node_modules/@angular/router/fesm2015/router.js");
    /* harmony import */


    var _services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./_services */
    "./src/app/_services/index.ts");

    var AppComponent =
    /*#__PURE__*/
    function () {
      function AppComponent(chRef, authenticationService, router) {
        var _this3 = this;

        _classCallCheck(this, AppComponent);

        this.chRef = chRef;
        this.authenticationService = authenticationService;
        this.router = router;
        this.showExample = false;
        this.actionText = '';
        this.authenticationService.currentToken.subscribe(function (x) {
          return _this3.currentToken = x;
        });
      }

      _createClass(AppComponent, [{
        key: "logout",
        value: function logout() {
          this.authenticationService.logout();
          this.router.navigate(['/login']);
        }
      }, {
        key: "ngOnInit",
        value: function ngOnInit() {
          this.navigationItems = [{
            title: 'Dashboard',
            iconStyleClass: 'fa fa-dashboard',
            url: '/terminal'
          }, {
            title: 'Infrastructures',
            iconStyleClass: 'fa pficon-service',
            url: '/iaas',
            badges: [{
              count: 85,
              tooltip: 'Total number of items'
            }]
          }, {
            title: 'Platforms',
            iconStyleClass: 'fa pficon-image',
            badges: [{
              count: 15,
              tooltip: 'Total number of items'
            }]
          }, {
            title: 'Settings',
            iconStyleClass: 'fa fa-paper-plane',
            id: 'mySettings',
            children: [{
              title: "Credentials",
              url: "/credentials",
              badges: [{
                count: 2,
                tooltip: "Total number of error items",
                iconStyleClass: 'pficon pficon-error-circle-o'
              }, {
                count: 6,
                tooltip: "Total number warning error items",
                iconStyleClass: 'pficon pficon-warning-triangle-o'
              }]
            }, {
              title: "Secrets",
              url: "/secrets",
              badges: [{
                count: 9,
                tooltip: "Total number of error items",
                iconStyleClass: 'pficon pficon-error-circle-o'
              }]
            }]
          }, {
            title: "Admin",
            iconStyleClass: "fa fa-map-marker",
            children: [{
              title: "Dashboard",
              url: "/admin/dashboard",
              badges: []
            }, {
              title: "Organizations",
              url: "/admin/organizations",
              badges: []
            }, {
              title: "Users",
              url: "/admin/users",
              badges: []
            }, {
              title: "IPAM",
              children: [{
                title: "Prefixes",
                url: "/admin/ipam/prefixes",
                badges: [{
                  count: 6,
                  tooltip: "Total number of error items",
                  badgeClass: 'example-error-background'
                }]
              }, {
                title: "Aggregates",
                url: "/admin/ipam/aggregates",
                badges: [{
                  count: 2,
                  tooltip: "Total number of items"
                }]
              }, {
                title: "Virtual RF",
                url: "/admin/ipam/vrfs",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "IP addresses",
                url: "/admin/ipam/ipaddresses",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "Vlans",
                url: "/admin/ipam/vlans",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "Internet Registries",
                url: "/admin/ipam/rirs",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "Devices",
                url: "/admin/ipam/devices",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "Virtual Machines",
                url: "/admin/ipam/virtualmachines",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "Network Gears",
                url: "/amet/detracto/principes",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }, {
                title: "Containers and Pods",
                url: "/admin/ipam/pods",
                badges: [{
                  count: 18,
                  tooltip: "Total number of warning items",
                  badgeClass: 'example-warning-background'
                }]
              }]
            }, {
              title: "SDN",
              url: "/admin/sdn",
              badges: []
            }, {
              title: "Storages",
              url: "/admin/storages",
              badges: []
            }, {
              title: "Services",
              url: "/admin/services",
              badges: []
            }, {
              title: "Monitorings",
              url: "/admin/monitorings",
              badges: []
            }, {
              title: "Security",
              url: "/admin/security",
              badges: []
            }, {
              title: "PKI",
              url: "/admin/pki",
              badges: []
            }, {
              title: "Backups",
              url: "/admin/backups",
              badges: []
            }, {
              title: "Billings",
              url: "/admin/billings",
              badges: []
            }, {
              title: "Documentations",
              url: "/admin/documentation",
              badges: []
            }, {
              title: "Configs",
              url: "/admin/configs",
              badges: []
            }]
          }];
        }
      }, {
        key: "toggleExample",
        value: function toggleExample() {
          this.showExample = !this.showExample;
          this.chRef.detectChanges();
        }
      }, {
        key: "onItemClicked",
        value: function onItemClicked($event) {
          this.actionText += 'Item Clicked: ' + $event.title + '\n';
        }
      }, {
        key: "onNavigation",
        value: function onNavigation($event) {
          this.actionText += 'Navigation event fired: ' + $event.title + '\n';
        }
      }]);

      return AppComponent;
    }();

    AppComponent.ctorParameters = function () {
      return [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"]
      }, {
        type: _services__WEBPACK_IMPORTED_MODULE_3__["AuthenticationService"]
      }, {
        type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]
      }];
    };

    AppComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
      encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewEncapsulation"].None,
      selector: 'app-root',
      template: tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! raw-loader!./app.component.html */
      "./node_modules/raw-loader/dist/cjs.js!./src/app/app.component.html")).default,
      styles: ["    \n    .faux-layout {\n      position: fixed;\n      top: 37px;\n      bottom: 0;\n      left: 0;\n      right: 0;\n      background-color: #f5f5f5;\n      padding-top: 15px;\n      z-index: 1100;\n    }\n    .example-page-container.container-fluid {\n      position: fixed;\n      top: 37px;\n      bottom: 0;\n      left: 0;\n      right: 0;\n      background-color: #f5f5f5;\n      padding-top: 15px;\n    }\n\n    .hide-vertical-nav {\n      margin-top: 15px;\n      margin-left: 30px;\n    }\n    \n    .navbar-brand-txt {\n      line-height: 34px;\n    }\n  "]
    })], AppComponent);
    /***/
  },

  /***/
  "./src/app/app.module.ts":
  /*!*******************************!*\
    !*** ./src/app/app.module.ts ***!
    \*******************************/

  /*! exports provided: AppModule */

  /***/
  function srcAppAppModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "AppModule", function () {
      return AppModule;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/platform-browser */
    "./node_modules/@angular/platform-browser/fesm2015/platform-browser.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/fesm2015/forms.js");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/fesm2015/http.js");
    /* harmony import */


    var _app_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! ./app-routing.module */
    "./src/app/app-routing.module.ts");
    /* harmony import */


    var _app_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ./app.component */
    "./src/app/app.component.ts");
    /* harmony import */


    var patternfly_ng_navigation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! patternfly-ng/navigation */
    "./node_modules/patternfly-ng/navigation/index.js");
    /* harmony import */


    var patternfly_ng_list__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! patternfly-ng/list */
    "./node_modules/patternfly-ng/list/index.js");
    /* harmony import */


    var ngx_bootstrap_dropdown__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! ngx-bootstrap/dropdown */
    "./node_modules/ngx-bootstrap/dropdown/fesm2015/ngx-bootstrap-dropdown.js");
    /* harmony import */


    var ngx_bootstrap_tooltip__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
    /*! ngx-bootstrap/tooltip */
    "./node_modules/ngx-bootstrap/tooltip/fesm2015/ngx-bootstrap-tooltip.js");
    /* harmony import */


    var _helpers__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
    /*! ./_helpers */
    "./src/app/_helpers/index.ts");
    /* harmony import */


    var _home__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
    /*! ./home */
    "./src/app/home/index.ts");
    /* harmony import */


    var _login__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
    /*! ./login */
    "./src/app/login/index.ts");
    /* harmony import */


    var _ahome_term_ahome_term_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
    /*! ./ahome-term/ahome-term.component */
    "./src/app/ahome-term/ahome-term.component.ts");
    /* harmony import */


    var _iaas_iaas_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
    /*! ./iaas/iaas.component */
    "./src/app/iaas/iaas.component.ts");
    /* harmony import */


    var _services_socketio_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
    /*! ./services/socketio.service */
    "./src/app/services/socketio.service.ts"); // NGX Bootstrap
    // socketio


    var AppModule = function AppModule() {
      _classCallCheck(this, AppModule);
    };

    AppModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
      declarations: [_app_component__WEBPACK_IMPORTED_MODULE_6__["AppComponent"], _ahome_term_ahome_term_component__WEBPACK_IMPORTED_MODULE_14__["AhomeTermComponent"], _iaas_iaas_component__WEBPACK_IMPORTED_MODULE_15__["IaasComponent"], _home__WEBPACK_IMPORTED_MODULE_12__["HomeComponent"], _login__WEBPACK_IMPORTED_MODULE_13__["LoginComponent"]],
      imports: [patternfly_ng_navigation__WEBPACK_IMPORTED_MODULE_7__["VerticalNavigationModule"], ngx_bootstrap_dropdown__WEBPACK_IMPORTED_MODULE_9__["BsDropdownModule"].forRoot(), ngx_bootstrap_tooltip__WEBPACK_IMPORTED_MODULE_10__["TooltipModule"].forRoot(), _angular_platform_browser__WEBPACK_IMPORTED_MODULE_2__["BrowserModule"], _app_routing_module__WEBPACK_IMPORTED_MODULE_5__["AppRoutingModule"], patternfly_ng_list__WEBPACK_IMPORTED_MODULE_8__["ListModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_3__["ReactiveFormsModule"], _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClientModule"]],
      providers: [{
        provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HTTP_INTERCEPTORS"],
        useClass: _helpers__WEBPACK_IMPORTED_MODULE_11__["JwtInterceptor"],
        multi: true
      }, {
        provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HTTP_INTERCEPTORS"],
        useClass: _helpers__WEBPACK_IMPORTED_MODULE_11__["ErrorInterceptor"],
        multi: true
      }, ngx_bootstrap_dropdown__WEBPACK_IMPORTED_MODULE_9__["BsDropdownConfig"], ngx_bootstrap_tooltip__WEBPACK_IMPORTED_MODULE_10__["TooltipConfig"], _services_socketio_service__WEBPACK_IMPORTED_MODULE_16__["SocketioService"] // provider used to create fake backend
      // fakeBackendProvider
      ],
      bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_6__["AppComponent"]]
    })], AppModule);
    /***/
  },

  /***/
  "./src/app/home/home.component.ts":
  /*!****************************************!*\
    !*** ./src/app/home/home.component.ts ***!
    \****************************************/

  /*! exports provided: HomeComponent */

  /***/
  function srcAppHomeHomeComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "HomeComponent", function () {
      return HomeComponent;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _app_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @app/_services */
    "./src/app/_services/index.ts");

    var HomeComponent =
    /*#__PURE__*/
    function () {
      function HomeComponent(userService) {
        _classCallCheck(this, HomeComponent);

        this.userService = userService;
        this.loading = false;
      }

      _createClass(HomeComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          var _this4 = this;

          this.loading = true;
          this.userService.getAll().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["first"])()).subscribe(function (users) {
            _this4.loading = false;
            _this4.users = users; // console.log(users)
          });
        }
      }]);

      return HomeComponent;
    }();

    HomeComponent.ctorParameters = function () {
      return [{
        type: _app_services__WEBPACK_IMPORTED_MODULE_3__["UserService"]
      }];
    };

    HomeComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
      template: tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! raw-loader!./home.component.html */
      "./node_modules/raw-loader/dist/cjs.js!./src/app/home/home.component.html")).default
    })], HomeComponent);
    /***/
  },

  /***/
  "./src/app/home/index.ts":
  /*!*******************************!*\
    !*** ./src/app/home/index.ts ***!
    \*******************************/

  /*! exports provided: HomeComponent */

  /***/
  function srcAppHomeIndexTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _home_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! ./home.component */
    "./src/app/home/home.component.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "HomeComponent", function () {
      return _home_component__WEBPACK_IMPORTED_MODULE_1__["HomeComponent"];
    });
    /***/

  },

  /***/
  "./src/app/iaas/iaas.component.css":
  /*!*****************************************!*\
    !*** ./src/app/iaas/iaas.component.css ***!
    \*****************************************/

  /*! exports provided: default */

  /***/
  function srcAppIaasIaasComponentCss(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony default export */


    __webpack_exports__["default"] = "";
    /***/
  },

  /***/
  "./src/app/iaas/iaas.component.ts":
  /*!****************************************!*\
    !*** ./src/app/iaas/iaas.component.ts ***!
    \****************************************/

  /*! exports provided: IaasComponent */

  /***/
  function srcAppIaasIaasComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "IaasComponent", function () {
      return IaasComponent;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var lodash__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! lodash */
    "./node_modules/lodash/lodash.js");
    /* harmony import */


    var lodash__WEBPACK_IMPORTED_MODULE_2___default =
    /*#__PURE__*/
    __webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_2__);
    /* harmony import */


    var _app_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @app/_services */
    "./src/app/_services/index.ts");

    var IaasComponent =
    /*#__PURE__*/
    function () {
      function IaasComponent(frontendService) {
        _classCallCheck(this, IaasComponent);

        this.frontendService = frontendService;
        this.actionsText = '';
        this.itemsAvailable = true;
        this.selectType = 'checkbox';
        this.htmlSnippet = ''; //  = 'Hello world!!';
      }

      _createClass(IaasComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          var _this5 = this;

          this.frontendService.getIaas().subscribe(function (data) {
            _this5.htmlSnippet = data;
          }); // console.log('pulic: ' + this.htmlSnippet );

          this.allItems = [{
            name: 'Fred Flintstone',
            address: '20 Dinosaur Way',
            city: 'Bedrock',
            state: 'Washingstone',
            typeIcon: 'fa-plane',
            clusterCount: 6,
            hostCount: 8,
            imageCount: 8,
            nodeCount: 10
          }, {
            name: 'John Smith',
            address: '415 East Main Street',
            city: 'Norfolk',
            state: 'Virginia',
            typeIcon: 'fa-magic',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8,
            hideExpandToggle: true
          }, {
            name: 'Frank Livingston',
            address: '234 Elm Street',
            city: 'Pittsburgh',
            state: 'Pennsylvania',
            typeIcon: 'fa-gamepad',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8
          }, {
            name: 'Linda McGovern',
            address: '22 Oak Street',
            city: 'Denver',
            state: 'Colorado',
            typeIcon: 'fa-linux',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8
          }, {
            name: 'Jim Brown',
            address: '72 Bourbon Way',
            city: 'Nashville',
            state: 'Tennessee',
            typeIcon: 'fa-briefcase',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8
          }, {
            name: 'Holly Nichols',
            address: '21 Jump Street',
            city: 'Hollywood',
            state: 'California',
            typeIcon: 'fa-coffee',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8
          }, {
            name: 'Marie Edwards',
            address: '17 Cross Street',
            city: 'Boston',
            state: 'Massachusetts',
            typeIcon: 'fa-rebel',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8
          }, {
            name: 'Pat Thomas',
            address: '50 Second Street',
            city: 'New York',
            state: 'New York',
            typeIcon: 'fa-linux',
            hostCount: 8,
            clusterCount: 6,
            nodeCount: 10,
            imageCount: 8
          }];
          this.items = Object(lodash__WEBPACK_IMPORTED_MODULE_2__["cloneDeep"])(this.allItems);
          this.emptyStateConfig = {
            actions: {
              primaryActions: [{
                id: 'action1',
                title: 'Main Action',
                tooltip: 'Start the server'
              }],
              moreActions: [{
                id: 'action2',
                title: 'Secondary Action 1',
                tooltip: 'Do the first thing'
              }, {
                id: 'action3',
                title: 'Secondary Action 2',
                tooltip: 'Do something else'
              }, {
                id: 'action4',
                title: 'Secondary Action 3',
                tooltip: 'Do something special'
              }]
            },
            iconStyleClass: 'pficon-warning-triangle-o',
            title: 'No Items Available',
            info: 'This is the Empty State component. The goal of a empty state pattern is to provide a good first ' + 'impression that helps users to achieve their goals. It should be used when a list is empty because no ' + 'objects exists and you want to guide the user to perform specific actions.',
            helpLink: {
              hypertext: 'List example',
              text: 'For more information please see the',
              url: '#/list'
            }
          };
        }
      }, {
        key: "ngDoCheck",
        value: function ngDoCheck() {}
        /**
         * Get the ActionConfig properties for each row
         *
         * @param item The current row item
         * @param actionButtonTemplate {TemplateRef} Custom button template
         * @param startButtonTemplate {TemplateRef} Custom button template
         * @returns {ActionConfig}
         */

      }, {
        key: "getActionConfig",
        value: function getActionConfig(item, actionButtonTemplate, startButtonTemplate) {
          var actionConfig = {
            primaryActions: [{
              id: 'start',
              styleClass: 'btn-primary',
              title: 'Start',
              tooltip: 'Start the server',
              template: startButtonTemplate
            }, {
              id: 'action1',
              title: 'Action 1',
              tooltip: 'Perform an action'
            }, {
              id: 'action2',
              title: 'Action 2',
              tooltip: 'Do something else'
            }, {
              id: 'action3',
              title: 'Action 3',
              tooltip: 'Do something special',
              template: actionButtonTemplate
            }],
            moreActions: [{
              id: 'moreActions1',
              title: 'Action',
              tooltip: 'Perform an action'
            }, {
              id: 'moreActions2',
              title: 'Another Action',
              tooltip: 'Do something else'
            }, {
              disabled: true,
              id: 'moreActions3',
              title: 'Disabled Action',
              tooltip: 'Unavailable action'
            }, {
              id: 'moreActions4',
              title: 'Something Else',
              tooltip: 'Do something special'
            }, {
              id: 'moreActions5',
              title: '',
              separator: true
            }, {
              id: 'moreActions6',
              title: 'Grouped Action 1',
              tooltip: 'Do something'
            }, {
              id: 'moreActions7',
              title: 'Grouped Action 2',
              tooltip: 'Do something similar'
            }],
            moreActionsDisabled: false,
            moreActionsVisible: true
          }; // Set button disabled

          if (item.started === true) {
            actionConfig.primaryActions[0].disabled = true;
          } // Set custom properties for row


          if (item.name === 'John Smith') {
            actionConfig.moreActionsStyleClass = 'red'; // Set kebab option text red

            actionConfig.primaryActions[1].visible = false; // Hide first button

            actionConfig.primaryActions[2].disabled = true; // Set last button disabled

            actionConfig.primaryActions[3].styleClass = 'red'; // Set last button text red

            actionConfig.moreActions[0].visible = false; // Hide first kebab option
          } // Hide kebab


          if (item.name === 'Frank Livingston') {
            actionConfig.moreActionsVisible = false;
          }

          return actionConfig;
        } // Actions

      }, {
        key: "handleAction",
        value: function handleAction($event, item) {
          if ($event.id === 'start' && item !== null) {
            item.started = true;
          }

          this.actionsText = $event.title + ' selected\r\n' + this.actionsText;
        }
      }, {
        key: "handleSelectionChange",
        value: function handleSelectionChange($event) {
          this.actionsText = $event.selectedItems.length + ' items selected\r\n' + this.actionsText;
        }
      }, {
        key: "handleClick",
        value: function handleClick($event) {
          this.actionsText = $event.item.name + ' clicked\r\n' + this.actionsText;
        }
      }, {
        key: "handleDblClick",
        value: function handleDblClick($event) {
          this.actionsText = $event.item.name + ' double clicked\r\n' + this.actionsText;
        } // Row selection

      }, {
        key: "updateItemsAvailable",
        value: function updateItemsAvailable() {
          this.items = this.itemsAvailable ? Object(lodash__WEBPACK_IMPORTED_MODULE_2__["cloneDeep"])(this.allItems) : [];
        }
      }]);

      return IaasComponent;
    }();

    IaasComponent.ctorParameters = function () {
      return [{
        type: _app_services__WEBPACK_IMPORTED_MODULE_3__["FrontendService"]
      }];
    };

    IaasComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
      encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewEncapsulation"].None,
      selector: 'app-iaas',
      template: tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! raw-loader!./iaas.component.html */
      "./node_modules/raw-loader/dist/cjs.js!./src/app/iaas/iaas.component.html")).default,
      styles: [tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! ./iaas.component.css */
      "./src/app/iaas/iaas.component.css")).default]
    })], IaasComponent);
    /***/
  },

  /***/
  "./src/app/login/index.ts":
  /*!********************************!*\
    !*** ./src/app/login/index.ts ***!
    \********************************/

  /*! exports provided: LoginComponent */

  /***/
  function srcAppLoginIndexTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _login_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! ./login.component */
    "./src/app/login/login.component.ts");
    /* harmony reexport (safe) */


    __webpack_require__.d(__webpack_exports__, "LoginComponent", function () {
      return _login_component__WEBPACK_IMPORTED_MODULE_1__["LoginComponent"];
    });
    /***/

  },

  /***/
  "./src/app/login/login.component.ts":
  /*!******************************************!*\
    !*** ./src/app/login/login.component.ts ***!
    \******************************************/

  /*! exports provided: LoginComponent */

  /***/
  function srcAppLoginLoginComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "LoginComponent", function () {
      return LoginComponent;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/router */
    "./node_modules/@angular/router/fesm2015/router.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/fesm2015/forms.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _app_services__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @app/_services */
    "./src/app/_services/index.ts");

    var LoginComponent =
    /*#__PURE__*/
    function () {
      function LoginComponent(formBuilder, route, router, authenticationService) {
        _classCallCheck(this, LoginComponent);

        this.formBuilder = formBuilder;
        this.route = route;
        this.router = router;
        this.authenticationService = authenticationService;
        this.loading = false;
        this.submitted = false;
        this.error = ''; // redirect to home if already logged in

        if (this.authenticationService.currentTokenValue) {
          this.router.navigate(['/']);
        }
      }

      _createClass(LoginComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          this.loginForm = this.formBuilder.group({
            username: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required]
          }); // get return url from route parameters or default to '/'

          this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
        } // convenience getter for easy access to form fields

      }, {
        key: "onSubmit",
        value: function onSubmit() {
          var _this6 = this;

          this.submitted = true; // stop here if form is invalid

          if (this.loginForm.invalid) {
            return;
          }

          this.loading = true;
          this.authenticationService.login(this.f.username.value, this.f.password.value).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["first"])()).subscribe(function (data) {
            _this6.router.navigate([_this6.returnUrl]);
          }, function (error) {
            _this6.error = error;
            _this6.loading = false;
          });
        }
      }, {
        key: "f",
        get: function get() {
          return this.loginForm.controls;
        }
      }]);

      return LoginComponent;
    }();

    LoginComponent.ctorParameters = function () {
      return [{
        type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"]
      }, {
        type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"]
      }, {
        type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]
      }, {
        type: _app_services__WEBPACK_IMPORTED_MODULE_5__["AuthenticationService"]
      }];
    };

    LoginComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
      template: tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"](__webpack_require__(
      /*! raw-loader!./login.component.html */
      "./node_modules/raw-loader/dist/cjs.js!./src/app/login/login.component.html")).default
    })], LoginComponent);
    /***/
  },

  /***/
  "./src/app/services/socketio.service.ts":
  /*!**********************************************!*\
    !*** ./src/app/services/socketio.service.ts ***!
    \**********************************************/

  /*! exports provided: SocketioService */

  /***/
  function srcAppServicesSocketioServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "SocketioService", function () {
      return SocketioService;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");

    var SocketioService = function SocketioService() {
      _classCallCheck(this, SocketioService);

      // this.socket = io(this.url);
      this.url = 'http://127.0.0.1:5000';
    };

    SocketioService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
      providedIn: 'root'
    })], SocketioService);
    /***/
  },

  /***/
  "./src/environments/environment.ts":
  /*!*****************************************!*\
    !*** ./src/environments/environment.ts ***!
    \*****************************************/

  /*! exports provided: environment */

  /***/
  function srcEnvironmentsEnvironmentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "environment", function () {
      return environment;
    });
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js"); // This file can be replaced during build by using the `fileReplacements` array.
    // `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
    // The list of file replacements can be found in `angular.json`.


    var environment = {
      production: false,
      apiUrl: 'http://127.0.0.1:8001'
    };
    /*
     * For easier debugging in development mode, you can import the following file
     * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
     *
     * This import should be commented out in production mode because it will have a negative impact
     * on performance if an error is thrown.
     */
    // import 'zone.js/dist/zone-error';  // Included with Angular CLI.

    /***/
  },

  /***/
  "./src/main.ts":
  /*!*********************!*\
    !*** ./src/main.ts ***!
    \*********************/

  /*! no exports provided */

  /***/
  function srcMainTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony import */


    var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! tslib */
    "./node_modules/tslib/tslib.es6.js");
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/fesm2015/core.js");
    /* harmony import */


    var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/platform-browser-dynamic */
    "./node_modules/@angular/platform-browser-dynamic/fesm2015/platform-browser-dynamic.js");
    /* harmony import */


    var _app_app_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./app/app.module */
    "./src/app/app.module.ts");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ./environments/environment */
    "./src/environments/environment.ts");

    if (_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].production) {
      Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["enableProdMode"])();
    }

    Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_2__["platformBrowserDynamic"])().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_3__["AppModule"]).catch(function (err) {
      return console.error(err);
    });
    /***/
  },

  /***/
  0:
  /*!***************************!*\
    !*** multi ./src/main.ts ***!
    \***************************/

  /*! no static exports found */

  /***/
  function _(module, exports, __webpack_require__) {
    module.exports = __webpack_require__(
    /*! /ahome_devel/ui/src/main.ts */
    "./src/main.ts");
    /***/
  }
}, [[0, "runtime", "vendor"]]]);
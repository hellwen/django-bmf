/*
 * AngularJS UI for django BMF
 *
 * Events:
 * --------------------------------------------------------
 *
 * All events listed here are fired upon $rootScope
 *
 * bmfRender(event, controller, html):
 * Instruction to load a Viewfunction via the (api/view)
 * needs to be fired with the API url of the targeted view
 *
 * bmfLoadView:
 * Instruction to load a Viewfunction via the (api/view)
 * needs to be fired with the API url of the targeted view
 *
 */

var app = angular.module('djangoBMF', []);

/*
 * Config
 */

app.config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $locationProvider.html5Mode(true).hashPrefix('!');
}]);

app.directive('bmfContent', ['$compile', function($compile) {
    return {
        restrict: 'A',
        priority: -500,
        link: function(scope, $element) {

            scope.$on('bmfRender', update);

            function update(event, controller, html) {
                if (controller && html) {
                    console.log("EVENT", controller, html, $element);
                    $element.html(html + ' [{{ testing }}]').show();
                    $compile($element.contents())(scope);
                }
            }
            update();
        }
    };
}]);

/*
 * Services
 */

/*
 * Unused
 */
/*
app.factory('bmfFindView', ['$location', '$rootScope', function bmfFindView($location, $rootScope) {
    return function(url) {
        if (url == undefined) {
            url = $location.path();
        }
        var current = null;
        $scope.BMFrameworkViewData.dashboards.forEach(function(d, dindex) {
            d.categories.forEach(function(c, cindex) {
                c.views.forEach(function(v, vindex) {
                    if (v.url == location.pathname) {
                        current = {
                            'view': v,
                            'category': c,
                            'dashboard': d
                        };
                    }
                });
            });
        });
        return current
  }
}]);
*/

/*
 * Controller
 */

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
app.controller('FrameworkCtrl', ['$http', '$rootScope', function($http, $rootScope) {

    // pace to store basic templates
    $rootScope.bmf_templates = {
        // template used to display items from the data api as a list
        'list': '',
    };

    // place to store all dashboards
    $rootScope.bmf_dashboards = undefined;

    // place to store all sitemaps
    $rootScope.bmf_sidebars = undefined;

    // holds the current dashboard
    $rootScope.bmf_current_dashboard = undefined;

    // holds all informations about the current view
    $rootScope.bmf_current_view = undefined

    // data holder
    $rootScope.bmf_data = undefined;

    // Load data from REST API
    var url = angular.element.find('body')[0].dataset.api;
    $http.get(url).then(function(response) {

        // Update sidebar and Dashboard objects
        var sidebar = {}
        response.data.dashboards.forEach(function(d, i) {
            sidebar[d.key] = d.categories;
        });
        $rootScope.bmf_dashboards = response.data.dashboards;
        $rootScope.bmf_sidebars = sidebar;
        $rootScope.bmf_templates = response.data.templates;

        // TODO: DEBUG
        $rootScope.bmf_current_dashboard = {key: 'sales', name:'SALES'};
    });


//  // TODO: MOVE TO FACTORY/SERVICE/ETC
//  $scope.get_view = function(url) {
//      if (url == undefined) {
//          url = $location.path();
//      }
//
//      var current = null;
//      $scope.BMFrameworkViewData.dashboards.forEach(function(d, dindex) {
//          d.categories.forEach(function(c, cindex) {
//              c.views.forEach(function(v, vindex) {
//                  if (v.url == location.pathname) {
//                      current = {
//                          'view': v,
//                          'category': c,
//                          'dashboard': d
//                      };
//                  }
//              });
//          });
//      });
//      if (current) {
//          $rootScope.bmf_current_dashboard = d.key;
//      }
//      return current
//  }

  //$scope.$on('$locationChangeStart', function(event, next, current) {
  //    console.log(event, next, current);
  //    if (next == current) {
  //        return true;
  //    }

  //    if ($location.protocol() == 'http' && $location.port() == 80) {
  //        var prefix = 'http://'+ $location.host();
  //    }
  //    else if ($location.protocol() == 'https' && $location.port() == 443) {
  //        var prefix = 'https://'+ $location.host();
  //    }
  //    else {
  //        var prefix = $location.protocol() + '://' + $location.host() + ':' + $location.port()
  //    }

////    // find if the url is managed by the framework
////    var url = null;
////    $scope.BMFrameworkViewData.dashboards.forEach(function(d, dindex) {
////        d.categories.forEach(function(c, cindex) {
////            c.views.forEach(function(v, vindex) {
////                if (prefix + v.url == next) {
////                    url = v.api;
////                }
////            });
////        });
////    });
////    if (url) {
////        $scope.$broadcast('BMFrameworkLoadView', url);
////        return true;
////    }
////
////    // prevent the default action, when leaving to a page which is not managed
////    // by the framework. using this will make the url reload on an history-back
////    // event

  //    event.preventDefault(true);
  //    $window.location = next;
  //});

//  $scope.$on('BMFrameworkLoadView', function(event, url) {
//      $http.get(url).then(function(response) {
//          console.log('LOADVIEW', response, response.data.html);
//      });
//  });
}]);

// This controller updates the dashboard dropdown menu
app.controller('DashboardCtrl', ['$scope', function($scope) {

    $scope.data = [];
    $scope.current_dashboard = null;

    $scope.$watch(
        function(scope) {return scope.bmf_current_dashboard},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );

    function update_dashboard() {
        var response = [];
        var current_dashboard = [];
        var key = $scope.bmf_current_dashboard.key;

        $scope.bmf_dashboards.forEach(function(d, di) {
            var active = false
            if (key == d.key) {
                active = true
            }

            response.push({
                'key': d.key,
                'name': d.name,
                'active': active,
            });
        });

        $scope.data = response;
        $scope.current_dashboard = $scope.bmf_current_dashboard;
    }
}]);

// This controller updates the dashboard dropdown menu
app.controller('SidebarCtrl', ['$scope', function($scope) {
    $scope.data = [];

    $scope.$watch(
        function(scope) {return scope.bmf_current_dashboard},
        function(newValue) {if (newValue != undefined) update_sidebar()}
    );

    function update_sidebar() {
        var response = [];
        var key = $scope.bmf_current_dashboard.key;

        response.push({
            'class': 'sidebar-board',
            'name': $scope.bmf_current_dashboard.name
        });

        $scope.bmf_sidebars[key].forEach(function(c, ci) {
            response.push({'name': c.name});
            c.views.forEach(function(v, vi) {
                response.push({'name': v.name, 'url': v.url});
                // TODO: Read if view is active
//              if (current_view && c.key == current_view.category.key && v.key == current_view.view.key) {
//                  response.push({'name': v.name, 'url': v.url, 'class': 'active'});
//                  $scope.$parent.$broadcast('BMFrameworkUpdateView', v, c, d);
//              }
//              else {
//                  response.push({'name': v.name, 'url': v.url});
//              }
            });
        });

        $scope.data = response;
    }
}]);

// TODO OLD
app.controller('bmfListCtrl', function($scope, $http) {
    $scope.$on('BMFrameworkUpdateView', function(event, view, category, dashboard) {
        var url = view.dataapi + '?d=' + dashboard.key + '&c=' + category.key + '&v=' + view.key
        $http.get(url).then(function(response) {
            $scope.data = response.data;
        });
    });
});

/*
 * ui-controller
 */

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
app.controller('FrameworkCtrl', ['$http', '$rootScope', '$scope', '$window', 'CurrentView', 'PageTitle', function($http, $rootScope, $scope, $window, CurrentView, PageTitle) {

    // pace to store basic templates
    $rootScope.bmf_templates = {
        // template used to display items from the data api as a list
        'list': '',
        'detail': '',
    };

    // place to store all dashboards
    $rootScope.PageTitle = PageTitle;

    // place to store all dashboards
    $rootScope.bmf_dashboards = undefined;

    // place to store all top navigation
    $rootScope.bmf_navigation = undefined;

    // place to store all sitemaps
    $rootScope.bmf_sidebars = undefined;

    // place to store all sitemaps
    $rootScope.bmf_modules = undefined;

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
        response.data.dashboards.forEach(function(element, index) {
            sidebar[element.key] = element.categories;
        });

        var modules = {}
        response.data.modules.forEach(function(element, index) {
            modules[element.ct] = element;
        });

        $rootScope.bmf_modules = modules;
        $rootScope.bmf_sidebars = sidebar;

        $rootScope.bmf_dashboards = response.data.dashboards;
        $rootScope.bmf_debug = response.data.debug;
        $rootScope.bmf_templates = response.data.templates;
        $rootScope.bmf_navigation = response.data.navigation;

        if (response.data.debug) {
            console.log("BMF-API", response.data);
        }

        CurrentView.update();
    });

    $scope.$on('$locationChangeStart', function(event, next, current) {
        // only invoke if dashboards are present (and the ui is loaded propperly)
        if ($rootScope.bmf_dashboards) {
            var next_view = CurrentView.get(next, true);
            if (next_view) {
                CurrentView.go(next_view);
                return true
            };
        }

        // Case when the target url is not managed by the ui
        event.preventDefault(true);
        if (next != current) {
            $window.location = next;
        }
    });
}]);

// This controller updates the dashboard dropdown menu
app.controller('DashboardCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {

    $scope.data = [];
    $scope.current_dashboard = null;

    $scope.$watch(
        function(scope) {return scope.bmf_dashboards},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );
    $scope.$watch(
        function(scope) {return scope.bmf_current_dashboard},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );

    function update_dashboard(key) {
        var response = [];
        var current_dashboard = [];
        var current = $scope.bmf_current_dashboard;

        $scope.bmf_dashboards.forEach(function(d, di) {
            var active = false
            if (current && current.key == d.key || key && key == d.key) {
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

    $scope.update = function(key) {
        var name;
        $scope.bmf_dashboards.forEach(function(d, di) {
            if (key && key == d.key) {
                name = d.name;
            }
        });

        if (name) {
            $rootScope.bmf_current_dashboard = {
                key: key,
                name: name
            };
        }
        else {
            $rootScope.bmf_current_dashboard = undefined;
        }
    };

}]);

// This controller updates the dashboard dropdown menu
app.controller('SidebarCtrl', ['$scope', function($scope) {
    $scope.data = [];

    $scope.$watch(
        function(scope) {return scope.bmf_current_view},
        function(newValue) {if (newValue != undefined && (newValue.type == "list" || newValue.type == "detail")) update_sidebar()}
    );
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
                if ($scope.bmf_current_view && ($scope.bmf_current_view.type == "list" || $scope.bmf_current_view.type == "detail") && c.key == $scope.bmf_current_view.category.key && v.key == $scope.bmf_current_view.view.key) {
                    response.push({'name': v.name, 'url': v.url, 'class': 'active'});
                }
                else {
                    response.push({'name': v.name, 'url': v.url});
                }
            });
        });

        $scope.data = response;
    }
}]);

// This controller manages the activity form
app.controller('ActivityFormCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.data = {};
    console.log($scope);
    $scope.processForm = function() {
        var url = $scope.$parent.$parent.ui.views.activity.url;
        $http({
            method: 'POST',
            data: $scope.data,
            url: url,
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
            // success callback
            // console.log("success", this, response);
            window.location.reload(); 
        }, function (response) {
            // error callback
            console.log("ActivityForm - Error", response);
            alert(response.data.non_field_errors[0]);
        })
    }
}]);


// This controller updates the dashboards navigation
app.controller('NavigationCtrl', ['$scope', '$interval', function($scope, $interval) {
    $scope.data = undefined;

    $scope.$watch(
        function(scope) {return scope.bmf_navigation && scope.bmf_navigation.length || 0},
        function(newValue) {if (newValue != undefined) init_navigation()}
    );

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        $scope.data.forEach(function(nav, i) {
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
        });
    });

    function init_navigation() {
        if (!$scope.bmf_navigation) return false;

        $scope.data = $scope.bmf_navigation;

        $scope.update = function (i) {
            nav = $scope.data[i]
            console.log("TIMER", i, nav)
        }

        $scope.data.forEach(function(nav, i) {
            // use the button as a link if url is set
            if (nav.url == undefined) nav.url = '#';

            // stop an old timer
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
            nav.timer = undefined;

            if (nav.api && nav.intervall) {
                $scope.update(i);
                nav.timer = $interval(function() {
                    $scope.update(i)
                }, nav.intervall * 1000);
            }
        });



//      var response = [];
//      var key = $scope.bmf_current_dashboard.key;
//
//      response.push({
//          'class': 'sidebar-board',
//          'name': $scope.bmf_current_dashboard.name
//      });
//
//      $scope.bmf_sidebars[key].forEach(function(c, ci) {
//          response.push({'name': c.name});
//          c.views.forEach(function(v, vi) {
//              if ($scope.bmf_current_view && $scope.bmf_current_view.type == "list" && c.key == $scope.bmf_current_view.category.key && v.key == $scope.bmf_current_view.view.key) {
//                  response.push({'name': v.name, 'url': v.url, 'class': 'active'});
//              }
//              else {
//                  response.push({'name': v.name, 'url': v.url});
//              }
//          });
//      });
//
        console.log($scope.data);
    }
}]);

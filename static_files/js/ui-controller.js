/*
 * ui-controller
 */

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
bmfapp.controller('FrameworkCtrl', ['$http', '$rootScope', '$scope', '$window', 'PageTitle', 'ViewUrlconf', function($http, $rootScope, $scope, $window, PageTitle, ViewUrlconf) {

    /**
     * @description
     *
     * This scope stores the base url to the API (needed for lookups)
     *
     */
    $rootScope.bmf_api_base = angular.element.find('body')[0].dataset.api;

    /**
     * @description
     *
     * This scope stores the currently active module
     *
     */
    $rootScope.bmf_module = undefined;

    /**
     * @description
     *
     * Every overlay get appended to this list. we only show one modal
     * per time and update the content as long as this list is not empty
     *
     * data
     * - TODO??
     *
     */
    $rootScope.bmf_modal = [];

    /**
     * @description
     *
     * The breadcrumbs are filled with data as the user navigates through the
     * framework. it contains information about the history to provide the
     * functionality to go back one page. With this we are able to travel
     * from a module to another without changing the overlaying view.
     * 
     * The listing pages overwrite this, while every detail-page appends to
     * this.
     *
     * data is generated via the ViewUrlconf factory
     * - name: the view callback name
     * - url: the called url
     * - kwargs: the views keyword arguments
     *
     */
    $rootScope.bmf_breadcrumbs = [];

    /**
     * @description
     *
     * The urlconf is needed to map an url to a view / controller (?)
     * TODO: check if if could be loaded via the REST-API
     *
     */
    $rootScope.bmf_view_urlconf = [
        {
            name: 'list',
            parent: null,
            regex: new RegExp('dashboard/([\\w-]+)/([\\w-]+)/([\\w-]+)/$'),
            args: ['dashboard', 'category', 'view'],
        },
        {
            name: 'detail',
            parent: 'list',
            regex: new RegExp('dashboard/([\\w-]+)/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['dashboard', 'category', 'view', 'pk'],
        },
        {
            name: 'notification',
            parent: null,
            regex: new RegExp('notification/$'),
            args: [],
        },
        {
            name: 'notification',
            parent: null,
            regex: new RegExp('notification/([\\w-]+)/([\\w-]+)/$'),
            args: ['app_label', 'model_name'],
        },
        {
            name: 'detail',
            parent: 'notification',
            regex: new RegExp('notification/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['app_label', 'model_name', 'pk'],
        },
    ];
    // TODO this is currenty unused
    $rootScope.bmf_api_urlconf = [
        {
            type: 'activity',
            pk: true,
        },
        {
            type: 'notification',
            action: 'list',
        },
        {
            type: 'notification',
            action: 'view',
        },
        {
            type: 'notification',
            action: 'view',
            pk: true,
        },
        {
            type: 'related',
            action: '?field',
            pk: true,
        },
    ];

    // pace to store basic templates
    /**
     * @description
     *
     * place where all templates are stored
     *
     */
    $rootScope.bmf_templates = {
        'list': '',
        'detail': '',
        'notification': '',
    };


    $rootScope.bmf_api = {
        base: angular.element.find('body')[0].dataset.api,
        app_label: undefined,
        model_name: undefined,
        module: undefined,
    };

    // place to store all dashboards
    $rootScope.PageTitle = PageTitle;

    // place to store all dashboards
    $rootScope.bmf_dashboards = undefined;

    // place to store all top navigation
    $rootScope.bmf_navigation = undefined;

    // place to store all sitemaps
    $rootScope.bmf_sidebars = undefined;

    $rootScope.bmf_modules = undefined;

    $rootScope.bmf_ui = undefined;

    $rootScope.bmf_last_dashboard = undefined;
    $rootScope.bmf_last_view = undefined

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

        $rootScope.bmf_ui = response.data.ui;
        $rootScope.bmf_dashboards = response.data.dashboards;
        $rootScope.bmf_debug = response.data.debug;
        $rootScope.bmf_templates = response.data.templates;
        $rootScope.bmf_navigation = response.data.navigation;

        if ($rootScope.bmf_debug) {
            console.log("BMF-API", response.data);
        }

        // load urlconf when all variables are set
        ViewUrlconf(window.location.href);
    });

    $scope.$on('$locationChangeStart', function(event, next, current) {
        if (!ViewUrlconf(next)) {
            // if the url is not managed by the framework, prevent default
            // action from the angularJS url management and redirect browser to the new url
            // if the url was changed
            event.preventDefault(true);
            if (next != current) {
                $window.location = next;
            }
        }
    });
}]);

// This controller updates the dashboard dropdown menu
bmfapp.controller('DashboardCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {

    $scope.data = [];
    $scope.current = undefined;

    $scope.$watch(
        function(scope) {return scope.bmf_dashboards},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );
    $scope.$watch(
        function(scope) {return scope.bmf_last_dashboard},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );

    function update_dashboard(key) {
        var response = [];
        var data = [];
        var current = undefined;
        if (!key && $scope.bmf_last_dashboard) key = $scope.bmf_last_dashboard.key;

        $scope.bmf_dashboards.forEach(function(d, di) {
            var active = false
            if (key && key == d.key) {
                active = true;
                current = d;
            }
            data.push({
                'key': d.key,
                'name': d.name,
                'active': active,
            });
        });

        $scope.data = data;
        $scope.current = current;
        $rootScope.bmf_current_dashboard = current;
    }
    $scope.update = update_dashboard;

}]);


// This controller updates the dashboard dropdown menu
bmfapp.controller('NotificationCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
    $scope.navigation = [];
    for (var key in $rootScope.bmf_modules) {
        $scope.navigation.push($rootScope.bmf_modules[key]);
    };
}]);

// This controller updates the dashboard dropdown menu
bmfapp.controller('SidebarCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
    $scope.data = [];

    $scope.$watch(
        function(scope) {return scope.bmf_current_view},
        function(newValue) {if (newValue != undefined && (newValue.type == "list" || newValue.type == "detail")) update_sidebar()}
    );
    $rootScope.$watch(
        function(scope) {return $rootScope.bmf_current_dashboard},
        function(value) {if (value != undefined) dashboard($rootScope.bmf_breadcrumbs[0], value.key, value.name)}
    );
    $rootScope.$watch(
        function(scope) {
            if ($rootScope.bmf_breadcrumbs.length == 0) return undefined;
            return $rootScope.bmf_breadcrumbs[0].url;
        },
        function(value) {if (value != undefined) update($rootScope.bmf_breadcrumbs[0]);}
    );

    function update(view) {
        if ($rootScope.bmf_debug) {
            console.log("ROOT-VIEW", view);
        }
    }

    function dashboard(root, key, name) {
        var data = []
        data.push({
            'class': 'sidebar-board',
            'name': name,
        });

        $rootScope.bmf_sidebars[key].forEach(function(c, ci) {
            data.push({'name': c.name});
            c.views.forEach(function(v, vi) {
                if ('dashboard' in root.kwargs && 'category' in root.kwargs && 'view' in root.kwargs && root.kwargs.dashboard == key && root.kwargs.category == c.key && root.kwargs.view == v.key) {
                    data.push({'name': v.name, 'url': v.url, 'class': 'active'});
                }
                else {
                    data.push({'name': v.name, 'url': v.url});
                }
            });
        });
        $scope.data = data;
    }

    function update_sidebar() {
        if (!$scope.bmf_current_dashboard) return false;
        dashboard(
            $rootScope.bmf_breadcrumbs[0],
            $scope.bmf_current_dashboard.key,
            $scope.bmf_current_dashboard.name
        );
    }
}]);

// This controller manages the activity form
bmfapp.controller('ActivityFormCtrl', ['$scope', '$http', function($scope, $http) {
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
        });
    }
}]);


// This controller updates the dashboards navigation
bmfapp.controller('NavigationCtrl', ['$scope', '$interval', function($scope, $interval) {
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
    }
}]);

/*
 * ui-factory
 */

// This factory uses the rootScope to generate a from a given type (req),
// action(opt) and primary_key(opt)
bmfapp.factory('ApiUrlFactory', ['$rootScope', function($rootScope) {
    return function(type, action, pk) {
        if (!$rootScope.bmf_api.base) throw "api not loaded";
        if (!$rootScope.bmf_api.app_label) throw "no app_label defined";
        if (!$rootScope.bmf_api.model_name) throw "no model_name defined";
        if (!type) throw "no type defined";
        var url = $rootScope.bmf_api.base + type + '/' + $rootScope.bmf_api.app_label + '/' + $rootScope.bmf_api.model_name + '/';
        if (action) url += action + '/';
        if (pk) url += pk + '/';
        return url
    }
}]);


/**
 * @description
 *
 * TODO
 *
 */
bmfapp.factory('ViewUrlconf', ['$rootScope', function($rootScope) {
    return function(url) {
        // https://gist.github.com/jlong/2428561
        var parser = document.createElement('a');
        parser.href = url;

        var urlconf = undefined
        $rootScope.bmf_view_urlconf.forEach(function(view, i) {
            if (view.regex.test(parser.pathname)) urlconf = view;
        });

        if (!urlconf) return false;

        var exp = urlconf.regex.exec(parser.pathname);
        var kwargs = {}
        var kwargs_parent = {}
        urlconf.args.forEach(function(arg, i) {
            kwargs[arg] = exp[i+1];
            if (arg != 'pk') kwargs_parent[arg] = exp[i+1];
        });

        // TODO add validation ... ?

        // Overwrite the breadcrumbs
        if (urlconf.parent == null) {
            $rootScope.bmf_breadcrumbs = [{
                name: urlconf.name,
                url: url,
                path: parser.pathname,
                kwargs: kwargs,
            }];
            return true
        }
        // Update the breadcrumbs if they are not defined
        else if ($rootScope.bmf_breadcrumbs.length == 0) {
            var regex = new RegExp('^(.*/)[0-9+]/$');
            $rootScope.bmf_breadcrumbs = [{
                name: urlconf.parent,
                url: regex.exec(parser.pathname)[1],
                path: regex.exec(parser.pathname)[1],
                kwargs: kwargs_parent,
            },{
                name: urlconf.name,
                url: url,
                path: parser.pathname,
                kwargs: kwargs,
            }];
            return true
        }
        // TODO walk over each breadcrumb until the path is matched
        // return matched path with updated url or append a new entry
        $rootScope.bmf_breadcrumbs.push({
            name: urlconf.name,
            url: url,
            path: parser.pathname,
            kwargs: kwargs,
        });
        return true
    }
}]);


bmfapp.factory('CurrentView', ['$rootScope', '$location', 'PageTitle', function($rootScope, $location, PageTitle) {
    function go(next) {
        $rootScope.bmf_current_view = next;
        if (next && ["list", "detail"].indexOf(next.type) >= 0) {
            PageTitle.set(next.dashboard.name + ' - ' + next.category.name + ' - ' + next.view.name);
            $rootScope.bmf_current_dashboard = {
                key: next.dashboard.key,
                name: next.dashboard.name
            };
        }
    }

    function update(url, prefix) {
        var current = get(url, prefix);
        go(current);
        return current
    }

    function get(url, prefix) {
        if (url == undefined) {
            url = $location.path();
        }
        if (prefix) {
            if ($location.protocol() == 'http' && $location.port() == 80) {
                prefix = 'http://'+ $location.host();
            }
            else if ($location.protocol() == 'https' && $location.port() == 443) {
                prefix = 'https://'+ $location.host();
            }
            else {
                prefix = $location.protocol() + '://' + $location.host() + ':' + $location.port()
            }
        }
        else {
            prefix = ''
        }
        var current = undefined;

        // LIST AND DETAIL
        $rootScope.bmf_dashboards.forEach(function(d, di) {
            d.categories.forEach(function(c, ci) {
                c.views.forEach(function(v, vi) {
                    var regex = new RegExp('^' + prefix + v.url + '([0-9]+)/$');

                    // check if the view relates to a list view
                    if (prefix + v.url == url) {
                        current = {
                            type: 'list',
                            view: v,
                            category: c,
                            dashboard: d,
                        };
                    }

                    // check if the view relates to a detail view
                    if (regex.test(url)) {
                        current = {
                            type: 'detail',
                            module: $rootScope.bmf_modules[v.ct],
                            pk: regex.exec(url)[1],
                            view: v,
                            category: c,
                            dashboard: d,
                        };
                    }
                });
            });
        });
        if (current) {
            return current;
        }
        // Notification index
        if (prefix + url == $rootScope.bmf_ui.notification.url) {
            return {
                type: 'notification',
                module: null,
            }
        }
        if (current) {
            return current;
        }
    }
    return {get: get, go: go, update: update}
}]);

bmfapp.factory('PageTitle', function() {
    var title = '';
    return {
        get: function() { return title; },
        set: function(newTitle) { title = newTitle }
    };
});

/*
 * ui-factory
 */

// This factory uses the rootScope to generate a from a given type (req),
// action(opt) and primary_key(opt)
bmfapp.factory('ApiUrlFactory', ['$rootScope', function($rootScope) {
    return function(module, type, action, pk) {
        if (!$rootScope.bmf_api.base) throw "api not loaded";
        if (!type) throw "no type defined";
        var url = $rootScope.bmf_api.base + type + '/';
        if (module) url += module.app + '/' + module.model + '/';
        if (action) url += action + '/';
        if (pk) url += pk + '/';
        return url
    }
}]);


/**
 * @description
 *
 * Get the dashboard from url parameters
 *
 */
bmfapp.factory('ViewFromUrl', ['$rootScope', function($rootScope) {
    return function(dashboard, category, view) {
        var data = undefined
        $rootScope.bmf_dashboards.forEach(function(d, di) {
            if (d.key == dashboard) d.categories.forEach(function(c, ci) {
                if (c.key == category) c.views.forEach(function(v, vi) {
                    if (v.key == view) {
                        data = {
                            view: v,
                            category: c,
                            dashboard: d,
                        }
                    }
                });
            });
        });
        return data
    }
}]);


/**
 * @description
 *
 * Get the module from url parameters
 *
 */
bmfapp.factory('ModuleFromUrl', ['$rootScope', function($rootScope) {
    return function(app_label, model_name) {
        var data = undefined
        for (var key in $rootScope.bmf_modules) {
            if ($rootScope.bmf_modules[key].app == app_label && $rootScope.bmf_modules[key].model == model_name ) return data = $rootScope.bmf_modules[key];
        };
        return data
    }
}]);


/**
 * @description
 *
 * Get the module from a content-type
 *
 */
bmfapp.factory('ModuleFromCt', ['$rootScope', function($rootScope) {
    return function(ct) {
        return $rootScope.bmf_modules[ct];
    }
}]);


/**
 * @description
 *
 * Parse the url, validate and update rootScope
 *
 */
bmfapp.factory('ViewUrlconf', ['$rootScope', 'ViewFromUrl', 'ModuleFromCt', 'ModuleFromUrl', function($rootScope, ViewFromUrl, ModuleFromCt, ModuleFromUrl) {
    return function(url) {
        // break if api is not loaded
        if (!$rootScope.bmf_dashboards || !$rootScope.bmf_modules) return false;

        // https://gist.github.com/jlong/2428561
        var parser = document.createElement('a');
        parser.href = url;

        var urlconf = undefined
        $rootScope.bmf_view_urlconf.forEach(function(view, i) {
            if (view.regex.test(parser.pathname)) urlconf = view;
        });

        if (!urlconf) return false;

        var exp = urlconf.regex.exec(parser.pathname);
        var kwargs = {};
        var kwargs_parent = {};
        urlconf.args.forEach(function(arg, i) {
            kwargs[arg] = exp[i+1];
            if (arg != 'pk') kwargs_parent[arg] = exp[i+1];
        });

        // Validation
        var view = undefined;
        var module = undefined;
        if ('app_label' in kwargs && 'model_name' in kwargs) {
            module = ModuleFromUrl(kwargs.app_label, kwargs.model_name);
            if (module == undefined) return false;
            $rootScope.bmf_module = module;
        }
        else if ('dashboard' in kwargs && 'category' in kwargs && 'view' in kwargs) {
            view = ViewFromUrl(kwargs.dashboard, kwargs.category, kwargs.view);
            if (view == undefined) return false;

            $rootScope.bmf_last_dashboard = {
                key: view.dashboard.key,
                name: view.dashboard.name
            };
            $rootScope.bmf_last_view = view;

            module = ModuleFromCt(view.view.ct);
            if (module == undefined) return false;
            $rootScope.bmf_module = module;

            // TODO REMOVE ME
            if ('pk' in kwargs) {
                $rootScope.bmf_current_view = {
                    type: urlconf.name,
                    module: module,
                    pk: kwargs.pk,
                    view: view.view,
                    category: view.category,
                    dashboard: view.dashboard,
                };
            }
            else {
                $rootScope.bmf_current_view = {
                    type: urlconf.name,
                    view: view.view,
                    category: view.category,
                    dashboard: view.dashboard,
                };
            }
        }

        // Fire event to update content layer
        // (needs to be fired before breadcrumbs are updated)
        $rootScope.bmfevent_content(urlconf.name);

        // Overwrite the breadcrumbs
        if (urlconf.parent == null) {
            $rootScope.bmf_breadcrumbs = [{
                name: urlconf.name,
                module: module || null,
                url: url,
                kwargs: kwargs,
            }];
        }
        // Update the breadcrumbs if they are not defined
        else if ($rootScope.bmf_breadcrumbs.length == 0) {
            var regex = new RegExp('^(.*/)[0-9+]/$');
            $rootScope.bmf_breadcrumbs = [{
                name: urlconf.parent,
                module: module || null,
                url: regex.exec(parser.pathname)[1],
                kwargs: kwargs_parent,
            },{
                name: urlconf.name,
                module: module || null,
                url: url,
                kwargs: kwargs,
            }];
        }
        else {
            // Walk over each breadcrumb until the path is matched
            // return matched path with updated url or append a new entry
            var index = undefined;
            $rootScope.bmf_breadcrumbs.forEach(function(crumb, i) {
                if (crumb.url == url) index = i;
            });
            if (index) for (var i=($rootScope.bmf_breadcrumbs.length - 1); i>index; $i--) {
                delete $rootScope.bmf_breadcrumbs[i];
            }

            $rootScope.bmf_breadcrumbs.push({
                name: urlconf.name,
                module: module || null,
                url: url,
                kwargs: kwargs,
            });
        }

        // fire events (with updated breadcrumbs)
        if (view) $rootScope.bmfevent_dashboard(kwargs.dashboard);

        return true
    }
}]);

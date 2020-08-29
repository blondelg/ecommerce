OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': 'Dashboard', 
        'icon': 'fas fa-chart-line', 
        'url_name': 'dashboard:index'
    },
    {
        'label': 'Products', 
        'icon': 'fas fa-store', 
        'url_name': 'dashboard:catalogue-product-list'
    },
    {
        'label': 'Orders', 
        'icon': 'fas fa-shopping-cart', 
        'url_name': 'dashboard:order-list'
    },

    {
        'label': 'Donations', 
        'icon': 'fas fa-donate',
        'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
        'children':[
            {
                'label': 'List', 
                'url_name': 'dashboard:donation-list'
            },
            {
                'label': 'Projects', 
                'url_name': 'dashboard:donation-project'
            }
        ]
    },

    {
        'label': 'Customers', 
        'icon': 'fas fa-users', 
        'url_name': 'dashboard:users-index'
    },
    {
        'label': 'Shipping', 
        'icon': 'fas fa-truck', 
        'url_name': 'dashboard:shipping-method-list'
    },
    {
        'label': 'Low stock alerts', 
        'icon': 'fas fa-exclamation-circle', 
        'url_name': 'dashboard:stock-alert-list'
    },
    {
        'label': 'Reviews', 
        'icon': 'fas fa-thumbs-up', 
        'url_name': 'dashboard:reviews-list'
    },
    {
        'label': 'Content Admin', 
        'icon': 'far fa-newspaper', 
        'url_name': 'wagtailadmin_home'
    },
    {
        'label': 'Data',  
        'icon': 'fas fa-file-csv', 
        'url_name': 'dashboard:reports-index'
    },
    {
        'label': 'Analytics',  
        'icon': 'fas fa-chart-bar', 
        'url_name': 'dashboard:reports-index'
    },

    {
        'label': 'Settings', 
        'icon': 'fas fa-cogs',
        'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
        'children':[
            {
                'label': 'Partners', 
                'url_name': 'dashboard:partner-list'
            },
            {
                'label': 'Product Types', 
                'url_name': 'dashboard:catalogue-class-list'
            },
            {
                'label': 'Product Categories', 
                'url_name': 'dashboard:catalogue-category-list'
            },
            {
                'label': 'Product Ranges', 
                'url_name': 'dashboard:range-list'
            },
            {
                'label': 'Stock alert', 
                'url_name': 'dashboard:user-alert-list'
            },
            {
                'label': 'Product Options', 
                'url_name': 'dashboard:catalogue-option-list'
            },
            {
                'label': 'Offers', 
                'url_name': 'dashboard:offer-list'
            },
            {
                'label': 'Coupons', 
                'url_name': 'dashboard:voucher-list'
            },
            {
                'label': 'Voucher Sets', 
                'url_name': 'dashboard:voucher-set-list'
            },
            {
                'label': 'Pages', 
                'url_name': 'dashboard:page-list'
            },
            {
                'label': 'Email templates', 
                'url_name': 'dashboard:comms-list'
            },
            {
                'label': 'Visualisation', 
                'url_name': 'dashboard:datavisu'
            },
            {
                'label': 'Statistics', 
                'url_name': 'dashboard:order-stats'
            },
        ]
    }
]

import copy
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponseForbidden
from .models import Permission

    
def login_perm_required(perm_check=True):
    """
    Checks the user is logged in, or else redirecting
    to the log-in page if necessary.
    If perm_check is true, checks whether a user has a particular permission
    enabled, or else given the PermissionDenied exception.
    """
    
    def decorator(view_func):
    
        def wrapped_view(cls, request, *args, **kwargs ):
            request_url = request.path_info
            if request.user.is_authenticated():
                if perm_check and request_url not in request.session[settings.PERMISSION_SESSION_KEY]:
                    return HttpResponseForbidden()
                return view_func(cls, request, *args, **kwargs)
            else:
                return HttpResponseRedirect( settings.LOGIN_URL + '?next=' + request_url )
        return wrapped_view
        
    return decorator

def set_user_permissions(request):
    """
    When user login successful, setting permissions in session
    """
    # Get user permissions
    permission_menu, permission_url_list = request.user.get_user_permissions()
    
    # set user session
    request.session[settings.MENU_SESSION_KEY] = permission_menu
    request.session[settings.PERMISSION_SESSION_KEY] = permission_url_list
        
def get_breadcrumb(menus, current_menu ):
    """
    Searching current  menu's all parent and change status
    arg: dict menus
    arg: menu-object current_menu
    return: list
    """
    breadcrumb = []
    position_tag = []
    def make_mark_posision(current_menu):
        breadcrumb.insert(0, current_menu)
        position_tag.insert(0, str(current_menu.id) )
        if not current_menu.parent:
            return
        make_mark_posision(current_menu.parent )
    make_mark_posision(current_menu)
        
    def change_marke_status(mark_menus):
 
        if not position_tag:
            return
            
        id = position_tag[0]
        if isinstance(mark_menus, dict):      # parent menu
            mark_menus[id]['status'] = True
            child_menus = mark_menus[id]['child'] if mark_menus[id].has_key('child') else []
        elif isinstance(mark_menus, list):    # traverse child menu and find pos that is marked.
            for menu in mark_menus:
                if int(menu['id'])  != int(id):
                    continue
                menu['status'] = True
                child_menus = menu['child'] if menu.has_key('child') else []
        position_tag.remove(id)
        change_marke_status( child_menus  )
    change_marke_status(menus)
    return breadcrumb
    
    
def get_page_menu(request):
    """
    Get user all permissions menu in the current page.
    Using this function that you should ensure user has login in.
    Here is the top menu and the left menu.You can adjust the menu tree for page layout.
    """
    top_menus = []
    breadcrumb = None
    current_menu_name = None
    request_url = request.path_info
    menus = copy.deepcopy(request.session[settings.MENU_SESSION_KEY])
    
    #Which buttons were clicked when you got to this step.
    current_menu = Permission.get_menu_by_request_url( request_url ) 
    if current_menu:
        current_menu_name = current_menu.name
        breadcrumb = get_breadcrumb(menus, current_menu)
        current_top_menuid = str(breadcrumb[0].id)
        current_siderbar_menus = menus[current_top_menuid].get('child', [])
    else:
        current_siderbar_menus = []
        
    for id, menu in menus.items():
        if menu.has_key('child'):
            menu.pop('child')
        top_menus.append(menu)
    
    return {
        'top_menus': top_menus,
        'breadcrumb': breadcrumb,
        'current_siderbar_menus': current_siderbar_menus,
        'current_menu_name': current_menu_name,
    }

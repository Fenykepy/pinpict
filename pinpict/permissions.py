from rest_framework import permissions



class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to edit object.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        
        return False



class IsStaffOrCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to list
    and retrieve object, and allow anybody to create new
    """

    def has_permission(self, request, view):
        # Create permissions are allowed to any request,
        # so we'll always allow POST, HEAD or OPTIONS requests.
        # admin user can GET or DELETE but can't PUT or PATCH resource
        ALLOWED_METHODS = ('POST', 'HEAD', 'OPTIONS')
        ADMIN_ALLOWED_METHODS = ('GET', 'DELETE')
        if request.method in ALLOWED_METHODS:
            return True
        if (request.user and request.user.is_staff and
                request.method in ADMIN_ALLOWED_METHODS):
            return True
        
        return False



class IsStaffOrAuthenticatedAndCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to list
    and retrieve object, and allow authenticated users to create new
    """

    def has_permission(self, request, view):
        # Create permissions are allowed to any request,
        # so we'll always allow POST, HEAD or OPTIONS requests.
        # admin user can GET or DELETE but can't PUT or PATCH resource
        ALLOWED_METHODS = ('HEAD', 'OPTIONS')
        AUTHENTICATED_ALLOWED_METHODS = ('POST', )
        ADMIN_ALLOWED_METHODS = ('GET', 'DELETE')
        if request.method in ALLOWED_METHODS:
            return True
        if (request.user and request.user.is_authenticated and
                request.method in AUTHENTICATED_ALLOWED_METHODS):
            return True
        if (request.user and request.user.is_staff and
                request.method in ADMIN_ALLOWED_METHODS):
            return True
        
        return False



class IsBoardAllowed(permissions.BasePermission):
    """
    Custom permission to only allow author to edit
    an object if he is it's owner, and to view an object if
    he is in a white list or if object is public.
    Assumes model instance has an `user` attribute.
    Assumes model instance has a `policy` attribute.
    Assumes model instance has a `users_can_read` attribute.
    """
   
    def has_object_permission(self, request, view, obj):
       SAFE_METHODS = ('HEAD', 'OPTIONS')
       PUBLIC_METHODS = ('GET', ) + SAFE_METHODS
       # HEAD and OPTIONS are allowed to anybody
       if request.method in SAFE_METHODS:
           return True
       # GET is allowed to public boards (policy == 1)
       if (request.method in PUBLIC_METHODS and
               obj.policy == 1):
           return True
       # Board's owner has full rights
       if (obj.user == request.user):
           return True
       # GET is allowed to private boards
       # if user is in white list
       if (request.method in PUBLIC_METHODS and
               request.user in obj.users_can_read):
           return True
       # Otherwise it's not allowed
       return False






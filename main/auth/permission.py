class Permission:

    def __init__(self, db, db_user, crud):
        self._db = db
        self._db_user = db_user
        self._crud = crud

    def can_view(self, route: str) -> bool:
        return View(db=self._db, db_user=self._db_user, crud=self._crud).has_permission(route=route)

class View(Permission): #NOTE: we should optimise this

    def __init__(self, db, db_user, crud):
        self._db = db
        self._db_user = db_user
        self._crud = crud

        self._role = self._crud.get_role_by_name(db=self._db, role_name=self._db_user.role)

    def has_permission(self, route: str) -> bool:
        if (route or '*' in self._role.can_view_routes['routes']):
            return True 
        return False
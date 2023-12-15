from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dungeonapi.views import UserViewSet, RaceViewSet, AlignmentViewSet, BackgroundViewSet, LanguageViewSet, SkillViewSet, AbilityViewSet, SavingThrowViewSet, FlawViewSet, IdealViewSet, BondViewSet, PersonalityTraitViewSet, DnDClassViewSet
from django.conf.urls.static import static
from .import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'races', RaceViewSet, "race")
router.register(r'alignments', AlignmentViewSet, "alignment")
router.register(r'backgrounds', BackgroundViewSet, "background")
router.register(r'languages', LanguageViewSet, "language")
router.register(r'skills', SkillViewSet, "skill")
router.register(r'abilities', AbilityViewSet, "ability")
router.register(r'savingthrows', SavingThrowViewSet, "savingthrow")
router.register(r'flaws', FlawViewSet, "flaw")
router.register(r'ideals', IdealViewSet, "ideal")
router.register(r'bonds', BondViewSet, "bond")
router.register(r'personalitytraits', PersonalityTraitViewSet, "personalitytrait")
router.register(r'dndclasses', DnDClassViewSet, "dndclass")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserViewSet.as_view({"post": "login_user"}), name='login'),
    path('register', UserViewSet.as_view({"post": "register_account"}), name='register')
]

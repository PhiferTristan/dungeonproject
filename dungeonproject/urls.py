from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dungeonapi.views import UserViewSet, RaceViewSet, AlignmentViewSet, BackgroundViewSet, LanguageViewSet, SkillViewSet, AbilityViewSet, SavingThrowViewSet, FlawViewSet, IdealViewSet, BondViewSet, PersonalityTraitViewSet, DnDClassViewSet, SubclassViewSet, DungeonMasterUserViewSet, PlayerUserViewSet, CharacterViewSet, CharacterAbilityScoreViewSet, CharacterSavingThrowViewSet, CharacterSkillViewSet
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
router.register(r'subclasses', SubclassViewSet, "subclass")
router.register(r'dungeonmasters', DungeonMasterUserViewSet, "dungeonmaster")
router.register(r'players', PlayerUserViewSet, "playeruser")
router.register(r'users', UserViewSet, 'user')
router.register(r'characters', CharacterViewSet, "character")
router.register(r'characterabilityscores', CharacterAbilityScoreViewSet, "characterabilityscore")
router.register(r'charactersavingthrows', CharacterSavingThrowViewSet, "charactersavingthrow")
router.register(r'characterskills', CharacterSkillViewSet, "characterskill")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserViewSet.as_view({"post": "login_user"}), name='login'),
    path('register', UserViewSet.as_view({"post": "register_account"}), name='register'),
    path('users/<pk>/update', UserViewSet.as_view({"put": "update_profile"}), name='update_profile')
]

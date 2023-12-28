from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dungeonapi.views import UserViewSet, RaceViewSet, AlignmentViewSet, BackgroundViewSet, LanguageViewSet, SkillViewSet, AbilityViewSet, SavingThrowViewSet, FlawViewSet, IdealViewSet, BondViewSet, PersonalityTraitViewSet, DnDClassViewSet, SubclassViewSet, DungeonMasterUserViewSet, PlayerUserViewSet, CharacterViewSet, CharacterAbilityScoreViewSet, CharacterSavingThrowViewSet, CharacterSkillViewSet, CharacterBackgroundViewSet, CharacterFlawViewSet, CharacterIdealViewSet, CharacterBondViewSet, CharacterPersonalityTraitViewSet
from django.conf.urls.static import static
from .import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'races', RaceViewSet, "race")
router.register(r'alignments', AlignmentViewSet, "alignment")
router.register(r'backgrounds', BackgroundViewSet, "background")
router.register(r'languages', LanguageViewSet, "language")
router.register(r'skills', SkillViewSet, "skill")
router.register(r'abilities', AbilityViewSet, "ability")
router.register(r'saving_throws', SavingThrowViewSet, "savingthrow")
router.register(r'flaws', FlawViewSet, "flaw")
router.register(r'ideals', IdealViewSet, "ideal")
router.register(r'bonds', BondViewSet, "bond")
router.register(r'personality_traits', PersonalityTraitViewSet, "personality_trait")
router.register(r'dndclasses', DnDClassViewSet, "dndclass")
router.register(r'subclasses', SubclassViewSet, "subclass")
router.register(r'dungeon_masters', DungeonMasterUserViewSet, "dungeon_master")
router.register(r'players', PlayerUserViewSet, "player_user")
router.register(r'users', UserViewSet, 'user')
router.register(r'characters', CharacterViewSet, "character")
router.register(r'character_ability_scores', CharacterAbilityScoreViewSet, "character_ability_score")
router.register(r'character_saving_throws', CharacterSavingThrowViewSet, "character_saving_throw")
router.register(r'character_skills', CharacterSkillViewSet, "character_skill")
router.register(r'character_backgrounds', CharacterBackgroundViewSet, "character_background")
router.register(r'character_flaws', CharacterFlawViewSet, "character_flaw")
router.register(r'character_ideals', CharacterIdealViewSet, "character_ideal")
router.register(r'character_bonds', CharacterBondViewSet, "character_bond")
router.register(r'character_personality_traits', CharacterPersonalityTraitViewSet, "character_personality_trait")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserViewSet.as_view({"post": "login_user"}), name='login'),
    path('register', UserViewSet.as_view({"post": "register_account"}), name='register'),
    path('users/<pk>/update', UserViewSet.as_view({"put": "update_profile"}), name='update_profile'),
    path('users/<pk>/delete', UserViewSet.as_view({"delete": "destroy_user"}), name='destroy_user')
]

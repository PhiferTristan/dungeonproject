from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dungeonapi.views import UserViewSet, RaceViewSet, AlignmentViewSet, BackgroundViewSet, LanguageViewSet, SkillViewSet, AbilityViewSet, SavingThrowViewSet, FlawViewSet, IdealViewSet, BondViewSet, PersonalityTraitViewSet, DnDClassViewSet, SubclassViewSet, DungeonMasterUserViewSet, PlayerUserViewSet, CharacterViewSet, CharacterAbilityScoreViewSet, CharacterSavingThrowViewSet, CharacterSkillViewSet, CharacterBackgroundViewSet, CharacterFlawViewSet, CharacterIdealViewSet, CharacterBondViewSet, CharacterPersonalityTraitViewSet, PartyViewSet
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
router.register(r'parties', PartyViewSet, "party")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserViewSet.as_view({"post": "login_user"}), name='login'),
    path('register', UserViewSet.as_view({"post": "register_account"}), name='register'),
    path('users/<pk>/update', UserViewSet.as_view({"put": "update_profile"}), name='update_profile'),
    path('users/<pk>/delete', UserViewSet.as_view({"delete": "destroy_user"}), name='destroy_user'),
    path('characters/', CharacterViewSet.as_view({'get': 'list'}), name='character-list'),
    path('characters/player/<int:player_id>/', CharacterViewSet.as_view({'get': 'list_for_player_user'}), name='list_for_player_user'),
    path('characters/<int:pk>/', CharacterViewSet.as_view({'get': 'retrieve'}), name='character-detail'),
    path('parties/', PartyViewSet.as_view({'get': 'list'}), name='party-list'),
    path('parties/player/<int:pk>/', PartyViewSet.as_view({'get': 'list_for_player_user'}), name='list_for_player_user'),
    path('parties/dungeon_master/<int:pk>/', PartyViewSet.as_view({'get': 'list_for_dungeon_master_user'}), name='list_for_dungeon_master_user'),
    path('parties/<int:pk>/remove_character/<int:character_id>/', PartyViewSet.as_view({'delete': 'remove_character'}), name='remove_character'),
    path('parties/<int:pk>/leave_party/<int:character_id>/', PartyViewSet.as_view({'delete': 'leave_party'}), name='leave_party'),
    path('parties/<int:pk>/add_character/', PartyViewSet.as_view({'put': 'add_character'}), name='add_character'),
]

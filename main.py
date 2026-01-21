from tetris.io.json_storage import JsonStorage
from ui.pygame_renderer import PygameRenderer
from ui.input_controller import InputController
from ui.scenes import SceneManager, MenuScene
from tetris.audio.audio_manager import AudioManager

def main() -> int:
    storage = JsonStorage()
    settings = storage.load_settings()

    renderer = PygameRenderer(settings)
    input_controller = InputController(settings)
    audio_manager = AudioManager(settings)

    manager = SceneManager(renderer=renderer, storage=storage, input_controller=input_controller, audio_manager=audio_manager)
    manager.set_scene(MenuScene(manager))

    try:
        manager.run()
    finally:
        audio_manager.shutdown()
        renderer.shutdown()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

from tetris.io.json_storage import JsonStorage
from tetris.ui.pygame_renderer import PygameRenderer
from tetris.ui.input_controller import InputController
from tetris.ui.scenes import SceneManager, MenuScene

def main() -> int:
    storage = JsonStorage()
    settings = storage.load_settings()

    renderer = PygameRenderer(settings)
    input_controller = InputController(settings)

    manager = SceneManager(renderer=renderer, storage=storage, input_controller=input_controller)
    manager.set_scene(MenuScene(manager))

    try:
        manager.run()
    finally:
        renderer.shutdown()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

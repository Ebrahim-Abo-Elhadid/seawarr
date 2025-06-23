
from model.mod import Model
from presenter.main import Presenter
from view.constants import SCREEN_RESOLUTION
from view.main import GeneralView
from audio.audiofi import AudioManager

def main():
    model = Model()

    # إنشاء وتشغيل مدير الأصوات
    audio_manager = AudioManager()
    audio_manager.play_background_music()

    # تمرير audio_manager للـ Presenter
    presenter = Presenter(model, audio_manager)
    view = GeneralView(presenter, model, SCREEN_RESOLUTION)

    while True:
        view.update()  
        presenter.handleEvents()

if __name__ == "__main__":
    main()



    
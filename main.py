from controller.app_controller import AppController
from view.main_view import MainView
from model.statistics_model import StatisticsModel

def main():
    model = StatisticsModel()
    view = MainView()
    controller = AppController(model, view)
    view.set_controller(controller)
    view.show_univariee_page()
    view.mainloop()

if __name__ == "__main__":
    main()

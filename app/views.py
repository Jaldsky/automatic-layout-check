from django.shortcuts import render, redirect

from app.libs.framework.views_base import ViewBase
# from app.сontroller import Controller
from app.forms import UserRegistrationForm, UserSettingsForm

from app.models import UserSettings


class MainPageView(ViewBase):
    PROHIBITED_METHODS: tuple = ('put', 'patch', 'delete')

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            user_settings = UserSettings.objects.get_or_create(username=request.user)[0]
            form = UserSettingsForm(instance=user_settings)
            return render(request, 'main/main_page.html', {'form': form})
        return render(request, 'main/wellcome_page.html')

    @staticmethod
    def post(request):
        form = Controller(request).exec()
        return render(request, 'main/main_page.html', {'form': form})






# def execute(request: WSGIRequest) -> render:
#     """Функция для выполнения основной логики.
#
#     Args:
#         request: запрос от сервера.
#     """
#     if request.method == 'POST':
#         settings = _update_settings(request.POST)
#         folder_path = _create_results_folder()
#         files_data = [upload_file_to_db(request, folder_path, 'pic'), upload_file_to_db(request, folder_path, 'zip')]
#         data = Controller().exec(files_data, folder_path)
#         if data:
#             data['main'] = settings
#         if ProjectSettings.objects.get().clear_local_cache:
#             _delete_dir(path.join(getcwd(), 'results'))
#         return render(request, 'main_page.html', data)
#     else:
#         form = FileUploadForm()
#     return render(request, 'main_page.html', {'form': form})




class UserRegistrationView(ViewBase):
    PROHIBITED_METHODS: tuple = ('put', 'patch', 'delete')
    INVALID_FORM_ERROR: str = 'Invalid form data provided'

    @staticmethod
    def get(request):
        form = UserRegistrationForm()
        return render(request, 'account/register_user.html', {'form': form})

    @staticmethod
    def post(request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'account/register_user.html', {'form': form})

# def compare(request: WSGIRequest) -> render:
#     if request.method == 'POST' and request.FILES['image']:
#         uploaded_image = request.FILES['image']
#         fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Путь к папке, где будет сохраняться файл
#         filename = fs.save(uploaded_image.name, uploaded_image)
#         # После сохранения файла можно выполнить дополнительные операции
#         # Например, сохранить путь к файлу в базе данных или выполнить какие-то другие действия
#
#         return HttpResponse("Картинка успешно загружена.")
#     else:
#         return HttpResponseBadRequest("Ошибка загрузки.")



# from app.models import UploadedFile, ProjectSettings
# from app.forms import FileUploadForm
#
# from app.engine.сontroller import Controller
#
#
# logger = logging.getLogger(__name__)
#
#
# def _create_results_folder() -> str:
#     """Функция для создания папки для хранения кеша.
#
#     Returns:
#         Путь до созданной папки.
#     """
#     folder_name = f'result {datetime.now().strftime("%d.%m %H-%M-%S")}'
#     folder_path = path.join(getcwd(), 'results', folder_name)
#     if not path.exists(folder_path):
#         makedirs(folder_path)
#     return folder_path
#
#
# def _move_uploaded_files(from_path: str, to_path: str) -> str:
#     """Функция для перемещения файлов.
#
#     Args:
#         from_path: путь до файла, который необходимо перенести.
#         to_path: путь для перемещения.
#
#     Returns:
#         Новый путь до файла.
#     """
#     return move(from_path, to_path)
#
#
# def _delete_dir(dir_path: str) -> None:
#     """Функция для удаления директории со всеми файлами и вложениями.
#
#     Args:
#         dir_path: путь до директории.
#     """
#     for file in listdir(dir_path):
#         file_path = path.join(dir_path, file)
#         try:
#             rmtree(file_path)
#         except Exception as e:
#             logger.error(f"Error deleting file {file_path}: {e}")
#
#
# def _update_settings(params: Dict) -> Dict:
#     """Функция для обновления настроек в проекте.
#
#     Args:
#         params: парамметры для сохранения.
#
#     Returns:
#         Словарь с сохраненными парамметрами.
#     """
#     project_settings = ProjectSettings.objects.first()
#     if project_settings is None:
#         return
#
#     project_settings.bedaub_text = bool(True if params.get('bedaub_text') else False)
#     project_settings.clear_local_cache = bool(True if params.get('clear_local_cache') else False)
#     project_settings.mse_comparator = bool(True if params.get('mse_comparator') else False)
#     project_settings.ssim_comparator = bool(True if params.get('ssim_comparator') else False)
#     project_settings.vgg16_comparator = bool(True if params.get('vgg16_comparator') else False)
#
#     project_settings.save()
#     return loads(str(project_settings))
#
#
# def upload_file_to_db(request: WSGIRequest, folder_path: str, upload_file_name: str) -> Union[Dict[str, str], None]:
#     """Функция для загрузки файла в базу данных.
#
#     Args:
#         request: запрос.
#         folder_path: путь до папки для хранения кеша.
#         upload_file_name: название файла.
#
#     Returns:
#         Словарь с сохраненными парамметрами.
#     """
#     file = request.FILES.get(upload_file_name, None)
#     if not file:
#         logger.error('File not found')
#         return None
#
#     file_extension = str(file).split('.')[-1]
#     file_name = str(file).replace(file_extension, '').strip('.')
#     uploaded_file = UploadedFile(name=file_name, type=file_extension)
#     uploaded_file.upload_to = folder_path
#     uploaded_file.save_file(file)
#
#     data = {'file_extension': file_extension, 'file_path': _move_uploaded_files(uploaded_file.file.path, folder_path)}
#     return data
#
#
# def execute(request: WSGIRequest) -> render:
#     """Функция для выполнения основной логики.
#
#     Args:
#         request: запрос от сервера.
#     """
#     if request.method == 'POST':
#         settings = _update_settings(request.POST)
#         folder_path = _create_results_folder()
#         files_data = [upload_file_to_db(request, folder_path, 'pic'), upload_file_to_db(request, folder_path, 'zip')]
#         data = Controller().exec(files_data, folder_path)
#         if data:
#             data['main'] = settings
#         if ProjectSettings.objects.get().clear_local_cache:
#             _delete_dir(path.join(getcwd(), 'results'))
#         return render(request, 'main_page.html', data)
#     else:
#         form = FileUploadForm()
#     return render(request, 'main_page.html', {'form': form})

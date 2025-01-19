from typing import Any, Literal, TypedDict

from numpy import ndarray
from playwright.sync_api._generated import Browser, Page
from playwright.sync_api import Playwright

Path = str

# typing for PlayWright class
Config = dict[str, Any]
Driver = Playwright
Browser = Browser
ScreenSavePath = Path
PageLocator = str
PlaywrightConfig = dict[str, Any]
PlayWrightPage = Page

# typing for Image class
ImgPath = Path
ImgSavePath = Path
ImgSize = tuple[int, int]
FromFormatImg = Literal["psd"]
ToFormatImg = Literal["png"]
ImgMatrix = ndarray

# typing for Comparator class
Similarity = float | int
SimilarityResult = float
ToGrayscale = float
FeatureMatrix = ndarray

class ComparatorResult(TypedDict):
    is_similar: str
    percent: float

# typing for ModelManager class
ModelName = str
RecordArgs = Any

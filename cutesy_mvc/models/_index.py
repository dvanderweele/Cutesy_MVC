from .BlogPost import BlogPost
from .Comment import Comment
from .Course import Course
from .Customer import Customer 
from .Hashtag import Hashtag
from .Image import Image
from .Phone import Phone
from .Schedule import Schedule
from .Student import Student
from .Tag import Tag
from .Tagable import Tagable
from .User import User
from .Video import Video

registry = {
    'BlogPost': BlogPost,
    'Comment': Comment,
    'Course': Course,
    'Customer': Customer,
    'Hashtag': Hashtag,
    'Image': Image,
    'Phone': Phone,
    'Schedule': Schedule,
    'Student': Student,
    'Tag': Tag,
    'Tagable': Tagable,
    'User': User,
    'Video': Video
}
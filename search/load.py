from searchTree import SearchTree
from dbInteractions.posts import TitleToIdDictOfAllPosts
from dbInteractions.users import usernameToIdDictOfAllUsers



postTitleToIdTree = SearchTree()
postTitleToIdTree.insertDict(TitleToIdDictOfAllPosts)

usernameToIdTree = SearchTree()
usernameToIdTree.insertDict(usernameToIdDictOfAllUsers)
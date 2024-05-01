from searchTree import SearchTree
from dbInteractions.posts import TitleToIdDictOfAllPosts



postTitleToIdTree = SearchTree()
postTitleToIdTree.insertDict(TitleToIdDictOfAllPosts)

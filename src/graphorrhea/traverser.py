from pathlib import PurePosixPath as Path

from graphorrhea.resources import Note, Notebook


class GitTraverser:
    def __init__(self, root):
        self.root = root

    def __call__(self, request):
        acidfs = request.acidfs
        path = Path(request.GET.get("path", "/"))
        context = None
        view_name = ""

        traversed = Path("/")
        for part in path.parts[1:]:
            if not acidfs.exists(str(traversed / part)):
                view_name = part
                break
            traversed /= part

        if acidfs.isdir(str(traversed)):
            context = Notebook(acidfs, str(traversed))
        else:
            context = Note(acidfs, str(traversed))

        return {
            "context": context,
            "root": self.root,
            "subpath": path.relative_to(traversed).parts,
            "traversed": traversed.parts[1:],
            "view_name": view_name,
            "virtual_root": self.root,
            "virtual_root_path": (),
        }

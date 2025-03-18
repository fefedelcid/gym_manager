import os
import sys
import git

# Variables
TARGET_BRANCH = "oxys-gym-branch"
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
SSH_KEY_PATH = os.path.join(REPO_PATH, 'app/utils/id_ed25519')

def set_ssh_key():
    """Configura la clave SSH para usar la Deploy Key."""
    os.environ['GIT_SSH_COMMAND'] = f'ssh -i {SSH_KEY_PATH} -o IdentitiesOnly=yes'

def update_system() -> bool:
    """Función que actualiza el sistema a la última versión del repositorio remoto."""
    repo = git.Repo(REPO_PATH)

    # Verifica si estamos en la rama correcta
    if repo.active_branch.name != TARGET_BRANCH:
        repo.git.checkout(TARGET_BRANCH)

    # Obtiene los últimos cambios
    repo.remotes.origin.fetch()

    # Verifica si hay cambios pendientes por aplicar
    commits_behind = len(list(repo.iter_commits(f"{repo.active_branch}..origin/{TARGET_BRANCH}")))
    if commits_behind > 0:
        print(f"Updating from remote, {commits_behind} commits behind.")
        # Realiza reset --hard para sobreescribir cambios locales
        repo.git.reset("--hard", "HEAD")

        # Realiza el merge con la rama remota
        repo.git.merge(f"origin/{TARGET_BRANCH}")
        print("Update complete.")
    else:
        print("No updates available.")
        return True



if __name__ == "__main__":
    # Configura la clave SSH para el acceso al repositorio
    set_ssh_key()

    # Ejecuta la actualización del sistema
    update_system()

    # Indica que la actualización ha finalizado correctamente
    sys.exit(0)

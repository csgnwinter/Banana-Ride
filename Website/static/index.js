function deleteNote(noteId){
    fetch('/delete-note1', {
        method: 'POST',
        body: JSON.stringify({ noteId:noteId }),
    }).then((_res) => {
        window.location.href = "/";
    })
}
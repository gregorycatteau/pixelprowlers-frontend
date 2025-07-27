// Basic Editor.js integration for the admin JSON field
// TODO: add HTML live preview below the field
// TODO: add a button to validate the block structure

function initEditorJS(textarea) {
  const holder = document.createElement('div');
  holder.classList.add('editorjs-holder');
  textarea.style.display = 'none';
  textarea.parentNode.insertBefore(holder, textarea.nextSibling);

  const editor = new EditorJS({
      holder: holder,
      data: textarea.value ? JSON.parse(textarea.value) : {},
      onChange: async () => {
          const output = await editor.save();
          textarea.value = JSON.stringify(output);
      }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('textarea.editorjs').forEach(initEditorJS);
});
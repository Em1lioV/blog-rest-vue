<template>
    <editor :api-key="apiKey" :init="editorOptions"></editor>
</template>

<script setup>
import Editor from '@tinymce/tinymce-vue';

const apiKey = process.env.VUE_APP_TINYMCEAPIKEY;

const editorOptions = {
  selector: 'textarea#post-content',
  plugins: 'print preview quickbars anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount save',
  toolbar: 'undo redo | searchreplace |bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange  formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment',
  width: "100%",
  language: 'es',
  height: 500,
  quickbars_insert_toolbar: false,
  menubar: 'file edit view insert format tools table tc help',
  quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote image quicktable',
  toolbar_mode: 'sliding',
  content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
  setup: function (editor) {
    editor.on('SaveContent', function () {
      console.log('save');
    });
  },
}

</script>

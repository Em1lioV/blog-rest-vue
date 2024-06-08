<template>
  <editor
    :id="field.id"
    :api-key="apiKey"
    :init="editorOptions"
    class="w-full"
  ></editor>
</template>

<script setup>
import Editor from "@tinymce/tinymce-vue";
import "@/assets/tailwind.css";
import { inject } from "vue";

const apiKey = process.env.VUE_APP_TINYMCEAPIKEY;

const editorOptions = {
  selector: "textarea#content",
  plugins:
    "print preview importcss searchreplace autolink save directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor insertdatetime lists  wordcount textpattern noneditable help charmap quickbars emoticons",
    menu: {
    file: { title: 'File', items: 'newdocument restoredraft | preview | export print | deleteallconversations' },
    edit: { title: 'Edit', items: 'undo redo | cut copy paste pastetext | selectall | searchreplace' },
    view: { title: 'View', items: 'code | visualaid visualchars visualblocks | spellchecker | preview fullscreen | showcomments' },
    insert: { title: 'Insert', items: 'image link media addcomment pageembed template codesample inserttable | charmap emoticons hr | pagebreak nonbreaking anchor tableofcontents | insertdatetime' },
    format: { title: 'Format', items: 'bold italic underline strikethrough superscript subscript codeformat | blocks fontfamily fontsize align lineheight | forecolor backcolor | language | removeformat' },
    tools: { title: 'Tools', items: 'spellchecker spellcheckerlanguage | a11ycheck code wordcount' },
    table: { title: 'Table', items: 'inserttable | cell row column | advtablesort | tableprops deletetable' },
    help: { title: 'Help', items: 'help' }
  },
  toolbar:
    "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment",
  image_advtab: true,
  automatic_uploads: false,
  importcss_append: true,
  content_css: [
    "https://cdn.jsdelivr.net/npm/@tailwindcss/typography@0.4.0/dist/typography.min.css",
    "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
  ],
  body_class: "prose p-5 w-full max-w-none",
  height: '100vh',
  image_caption: true,
  quickbars_selection_toolbar:
    "bold italic | quicklink h2 h3 blockquote codesample quickimage quicktable",
  toolbar_mode: "sliding",
  spellchecker_ignore_list: ["Ephox", "Moxiecode"],
  contextmenu: "link image in",
  a11y_advanced_options: true,
  setup: function (editor) {
    editor.on("SaveContent", function () {
      emit("save-content");
    });
    editor.on("init", function () {
      emit("editor-loaded");
    });
    
  },
};

const props = defineProps({
  required: Boolean,
  invalid: Boolean,
});

const emit = defineEmits(["editor-loaded","save-content"]);

const field = inject("field", props);
</script>



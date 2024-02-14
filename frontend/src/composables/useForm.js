import { reactive } from "vue";
import {  serialize } from 'object-to-formdata';
 
export default function useForm(fields) {
  return reactive({
    fields,
    processing: false,
    error: null,
    async submit(submitter) {
      if (this.processing) return;
 
      this.error = null;
      this.processing = true;
      
      const formData = serialize(this.fields);
      try {
        await submitter(formData);
      } catch (err) {
        console.log(err);
        this.error = err;
      }
 
      this.processing = false;
    },
  });
}

//@ts-nocheck

import React, { useEffect, useState } from "react";

interface args {
  requestFunc: (data: FormData) => Promise<void>;
  formFields: Array<any>;
}

export const useForm = ({ requestFunc, formFields }: args) => {
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [formError, setFormError] = useState<string | null>(null);

  //reset form error and submitting state on re render
  useEffect(() => {
    setSubmitting(false);
    setFormError(null);
  }, []);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    console.log("handling submit");
    setSubmitting(true);
    setFormError(null);
    const data: FormData = gatherFormDataUsingFields(e);
    requestFunc(data)
      .then((response) => {
        setSubmitting(false);
      })
      .catch((error) => {
        setSubmitting(false);
        if (error !== undefined) setFormError(error.message);
        else setFormError("An error occurred.");
      });
  };

  const gatherFormDataUsingFields = (
    e: React.FormEvent<HTMLFormElement>
  ): FormData => {
    const data = new FormData();
    formFields.map((field) => {
      data.append(field.name, e.target[field.name].value);
    });
    console.log("submitted values");
    data.forEach((v) => console.log(v));
    return data;
  };

  return {
    formError: formError,
    submitting: submitting,
    handleSubmit: handleSubmit,
  };
};

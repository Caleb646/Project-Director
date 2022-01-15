import React from "react";

import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import Alert from "@material-ui/lab/Alert";
import LoadingButton from "@material-ui/lab/LoadingButton";
import SendIcon from "@material-ui/icons/Send";

import { useForm } from "../../hooks";
import { PasswordField } from "../../components";
import { getKey } from "../../utils";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%",
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

interface formField {
  name: string;
  label: string;
  type: string | undefined;
  autoComplete: string;
}

interface Props {
  requestFunc: (data: FormData) => Promise<void>;
  submitBtnLabel: string;
  formFields: Array<formField>;
}

const BaseForm: React.FC<Props> = ({
  requestFunc,
  formFields,
  submitBtnLabel,
}) => {
  const classes = useStyles();
  const { formError, submitting, handleSubmit } = useForm({
    requestFunc,
    formFields,
  });

  const createFormFromFields = (): JSX.Element => {
    return (
      <>
        {formFields.map((field) => {
          if (field.type === "password")
            return (
              <Grid key={getKey()} item xs={12}>
                <PasswordField />
              </Grid>
            );
          return (
            <Grid key={getKey()} item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name={field.name}
                label={field.label}
                id={field.name}
                autoComplete={field.autoComplete}
              />
            </Grid>
          );
        })}
      </>
    );
  };

  return (
    <form onSubmit={handleSubmit} className={classes.form}>
      <Grid container spacing={2}>
        {createFormFromFields()}
      </Grid>
      <LoadingButton
        endIcon={<SendIcon />}
        pending={submitting}
        pendingPosition="end"
        variant="contained"
        color="primary"
        className={classes.submit}
        type="submit"
        fullWidth
      >
        {submitBtnLabel}
      </LoadingButton>
      {formError === null ? null : <Alert severity="error">{formError}</Alert>}
    </form>
  );
};

export default BaseForm;

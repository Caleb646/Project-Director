import React from "react";

import { useRouter } from "next/router";

import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import { ApiClient, BaseForm, fPaths, apiPaths, Header } from "../../src";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
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
      marginTop: theme.spacing(3),
    },
    submit: {
      margin: theme.spacing(3, 0, 2),
    },
  })
);

interface Props {}

const navLinks = [{ title: `Login`, path: fPaths.login }];

const Register: React.FC<Props> = () => {
  const classes = useStyles();
  const router = useRouter();
  const r = (data: FormData): Promise<void> =>
    ApiClient.post(apiPaths.register, data).then((response) => {
      router.push(fPaths.waitForConfirmEmail);
      return Promise.resolve();
    });
  const formProps = {
    requestFunc: r,
    submitBtnLabel: "Register",
    formFields: [
      {
        name: "email",
        label: "Email Address",
        type: "",
        autoComplete: "email",
      },
    ],
  };

  return (
    <>
      <Header links={navLinks} />
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          {/* <Avatar className={classes.avatar}>
              <LockOutlinedIcon />
            </Avatar> */}
          <Typography component="h1" variant="h5">
            Sign Up
          </Typography>
          <BaseForm {...formProps} />
        </div>
      </Container>
    </>
  );
};

export default Register;

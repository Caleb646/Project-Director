import React, { useEffect } from "react";

import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import {
  useAuthContext,
  useAuth,
  BaseForm,
  fPaths,
  apiPaths,
  Header,
} from "../../src";

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

const navLinks = [{ title: `Sign up`, path: fPaths.register }];

interface Props {}

const Login: React.FC<Props> = () => {
  const classes = useStyles();
  const { login } = useAuthContext();
  const r = (data: FormData) => login(data);
  const formProps = {
    requestFunc: r,
    submitBtnLabel: "Login",
    formFields: [
      {
        name: "email",
        label: "Email Address",
        type: "",
        autoComplete: "email",
      },
      {
        name: "password",
        label: "Password",
        type: "password",
        autoComplete: "password",
      },
    ],
  };
  //check if user is authenticated
  useAuth(true, fPaths.rfiManager, null);

  return (
    <>
      <Header links={navLinks} />
      <Container component="main" maxWidth="xs">
        <div className={classes.paper}>
          {/* <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar> */}
          <Typography component="h1" variant="h5">
            Login
          </Typography>
          <BaseForm {...formProps} />
        </div>
      </Container>
    </>
  );
};

export default Login;

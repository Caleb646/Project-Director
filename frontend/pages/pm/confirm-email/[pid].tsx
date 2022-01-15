import React from "react";

import { useRouter } from "next/router";

import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import { useAuthContext, BaseForm, fPaths } from "../../../src";

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

const ConfirmRegistration: React.FC<Props> = () => {
  const classes = useStyles();
  const router = useRouter();
  const { register } = useAuthContext();
  const { pid } = router.query;
  const r = (data: FormData) => {
    data.append("email", pid as string);
    return register(data).then((response: any) =>
      router.push(fPaths.emailConfirmed)
    );
  };
  const formProps = {
    requestFunc: r,
    submitBtnLabel: "Confirm Registration",
    formFields: [
      {
        name: "password",
        label: "Password",
        type: "password",
        autoComplete: "password",
      },
    ],
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
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
  );
};

export default ConfirmRegistration;

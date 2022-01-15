import { useEffect, useState } from "react";

import { useRouter } from "next/router";

import axios from "axios";

import { fPaths } from "../components";
import { useAuthContext } from "..";

export const useAuth = (
  redirectOnSuccess: boolean,
  successUrl: string,
  deps?: any
) => {
  /*
  1. use initAuth to determine if the user is authenticated.
  2. If the user is authenticated and redirectOnSuccess is true redirect
  the user to successUrl
  3. Else if the user is not authenticated redirect them to the login page.
  */

  //the signal is keep requests from continuing after a
  //component has already been unmounted.
  const signal = axios.CancelToken.source();
  const { initAuth, isAuthenticated } = useAuthContext();
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const auth = async () => {
    setLoading(true);
    await initAuth(signal);
    setLoading(false);
  };
  useEffect(() => {
    auth();
    return () => {
      //clean up hanging or slow requests.
      signal.cancel("Request was cancelled");
    };
  }, [deps]);

  useEffect(() => {
    //wait for initAuth to finish before redirecting anywhere.
    if (loading === false) {
      if (isAuthenticated === true && redirectOnSuccess === true)
        router.push(successUrl);
      else if (isAuthenticated === false) router.push(fPaths.login);
    }
  }, [isAuthenticated]);
};

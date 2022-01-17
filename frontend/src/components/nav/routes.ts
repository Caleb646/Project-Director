const apiUrl = process.env.NEXT_PUBLIC_API_URL + "/api/d1"; //"http://localhost:8080/api/d1"; //process.env.API_PATH;

export const fPaths = {
  home: "/",
  about: "#about",
  contact: "#contact",
  platformer: "#platformer",
  login: "/pm/login/",
  rfiManager: "/pm/",
  register: "/pm/register/",
  waitForConfirmEmail: "/pm/wait-email-confirm/",
  confirmRegistration: "/pm/confirm-registration/",
  emailConfirmed: "/pm/email-confirmed/",
};

export const apiPaths = {
  login: `${apiUrl}/auth/user/login/`,
  logout: `${apiUrl}/auth/user/logout/`,
  tokenRefresh: `${apiUrl}/auth/token/refresh/`,
  whoAmI: `${apiUrl}/pm/user/who_am_i`,
  register: `${apiUrl}/auth/user/register/`,
  confirmRegistration: `${apiUrl}/auth/user/confirm_registration/`,

  allGroups: `${apiUrl}/pm/group/`,

  allUsers: `${apiUrl}/pm/user/`,
  usersByJob: (id: number) => `${apiUrl}/pm/user/?job=${id}`,
  usersById: (id: number) => `${apiUrl}/pm/user/${id}/`,
  userCreateInvite: `${apiUrl}/pm/user/invite_user/`,
  userUpdate: (id: number) => `${apiUrl}/pm/user/${id}/`,

  jobs: `${apiUrl}/pm/job/`,
  allRfis: `${apiUrl}/pm/rfi/`,
  rfisByJob: (id: number) => `${apiUrl}/pm/rfi/?job_key=${id}`,
};

import { dataTypes } from ".";

type Group = {
  id: number;
  name: string;
};

interface GroupList {
  results: Array<Group>;
}

interface BaseUser {
  id: number;
  email: string;
}

interface DetailedUser {
  id: number;
  email: string;
  groups: Array<Group>;
  is_staff: boolean;
  is_active: boolean;
}

interface UserList {
  results: Array<DetailedUser> | [];
}

interface UserDetail {
  results: [
    {
      id: number;
      email: string;
      first_name: string;
      last_name: string;
      groups: Array<Group>;
      job_set: Array<BaseJob>;
      is_staff: boolean;
      is_active: boolean;
    }
  ];
}

interface BaseRFI {
  id: number;
  subject: string;
  date_created: string | Date;
  closed: boolean;
  f_user: BaseUser;
  t_user: Array<BaseUser>;
}

interface PaginatedResults {
  count: number;
  next: string | null; //url
  previous: string | null; //url
}

interface RFIList extends PaginatedResults {
  results: Array<BaseRFI> | [];
}

interface BaseJob {
  id: number;
  name: string;
  date_created: string | Date;
}

interface JobList {
  results: Array<BaseJob>;
}

export {
  Group,
  GroupList,
  BaseUser,
  DetailedUser,
  UserList,
  UserDetail,
  BaseRFI,
  RFIList,
  BaseJob,
  JobList,
};

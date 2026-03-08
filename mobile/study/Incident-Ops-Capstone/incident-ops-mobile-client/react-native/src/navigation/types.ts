export type AuthStackParamList = {
  Login: undefined;
};

export type IncidentStackParamList = {
  IncidentFeed: undefined;
  CreateIncident: undefined;
  IncidentDetail: {
    incidentId: string;
  };
};

export type MainTabParamList = {
  IncidentsTab: undefined;
  Approvals: undefined;
  Outbox: undefined;
  Settings: undefined;
};

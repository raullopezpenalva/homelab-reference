import jenkins.model.Jenkins
// Preserve the setup wizard and authentication. Builds require a separate agent.
Jenkins.get().setNumExecutors(0)
Jenkins.get().save()

pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        dockerfile {
          filename 'Dockerfile'
          label 'service-agent'
          args '--network internal'
        }
      }
      environment {
        REDIS_HOST = 'redis'
      }
      steps {
        sh 'make test'
      }
    }
  }
}

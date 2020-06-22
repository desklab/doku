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
    stage('Build') {
      when {
        beforeAgent true
        anyOf {
          branch 'master'
        }
      }
      agent {
        label 'service-agent'
      }
      environment {
        REGISTRY = credentials('desklab-registry')
      }
      steps {
        sh 'docker build -t reg.desk-lab.de/doku -t reg.desk-lab.de/doku:$GIT_COMMIT .'
        sh 'cd doku/static && docker build -t reg.desk-lab.de/doku-static -t reg.desk-lab.de/doku-static:$GIT_COMMIT .'
        sh 'docker login https://reg.desk-lab.de --username $REGISTRY_USR --password $REGISTRY_PSW'
        sh 'docker push reg.desk-lab.de/doku-static'
        sh 'docker push reg.desk-lab.de/doku-static:$GIT_COMMIT'
        sh 'docker push reg.desk-lab.de/doku'
        sh 'docker push reg.desk-lab.de/doku:$GIT_COMMIT'
      }
    }
  }
}


module.exports = function(grunt){
  grunt.initConfig({
    stylus:{
      compile: {
        files: {
          'erp/static/dashboard/main.css':'frontend/main.styl',
        },
      },
    },
    coffee: {
      compile: {
        files: [
          {
            expand: true,
            cwd: 'frontend/',
            src: ['**.coffee'],
            dest: 'frontend/',
            ext: '.js',
          },
        ],
      },
    },
    concat: {
      dist: {
        src: ['frontend/components/Claimsheet/template.vue','frontend/components/Claimsheet/core.vue'],
	dest: 'frontend/components/ClaimsheetEmployeeView.vue'
      }
    },
    browserify: {
      dist:{
        files: {
          'erp/static/dist/build.js': ['frontend/main.js'],
        },
        options: {
          transform: ['vueify'],
        },
      },
    },
    uglify: {
      compile: {
        files: {
          'erp/static/dist/build.min.js': ['erp/static/dist/build.js']
        }
      }
    },
    watch: {
      scripts : {
        files: ['frontend/*.styl','frontend/*.coffee','frontend/components/*.vue','frontend/components/Claimsheet/*.vue'],
          tasks: ['stylus','coffee','concat','browserify','uglify'],
	  options: {
            event: ['new','changed'],
	  },
      },
	
    },
  });
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-pug');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-stylus');
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('default',['stylus','coffee','concat','browserify','uglify','watch']);
};

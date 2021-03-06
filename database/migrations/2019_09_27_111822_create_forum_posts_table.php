<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateForumPostsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('forum_posts', function (Blueprint $table) {
            $table->uuid('id')->primary();

            $table->longText('body');

            $table->integer('user_id')->unsigned();
            $table->uuid('status_id');
            $table->uuid('forum_id');
            $table->uuid('parent_id');

            $table->boolean('is_parent');
            $table->boolean('is_question_and_answer');
            $table->boolean('is_sticky_post');

            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('forum_posts');
    }
}

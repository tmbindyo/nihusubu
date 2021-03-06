<?php

namespace App;

use App\Traits\UuidTrait;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Section extends Model
{
    use SoftDeletes, UuidTrait;
    public $incrementing = false;

    // Parents
    public function status()
    {
        return $this->belongsTo('App\Status');
    }
    public function user()
    {
        return $this->belongsTo('App\User');
    }

    // Children
    public function menus()
    {
        return $this->hasMany('App\Menu');
    }
    public function user_type_sections()
    {
        return $this->hasMany('App\UserTypeSection');
    }
    public function role_user_type_sections()
    {
        return $this->hasMany('App\RoleUserTypeSection');
    }
}
